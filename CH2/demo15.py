import ollama
import chromadb
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
import pdfplumber

# 初始化 ChromaDB
client = chromadb.Client() # 預設使用本地ram儲存
# 建立集合
collection = client.create_collection(name="docs")

embedding_model = "nomic-embed-text"
genrenator_model = "llama3.2:3b"

def embed_document(file_path, chunk_size=1000, chunk_overlap=200):
    try:
        content = ""
        # 讀取 PDF 文件
        with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    content += page.extract_text() or "" + "\n\n"

        # 如果內容為空，可能是PDF無法提取文本，例如是掃描的圖像
        if not content.strip():
            print("警告：無法從PDF提取文本，可能需要使用OCR技術")
            return False
            
        # 使用 LangChain 的 RecursiveCharacterTextSplitter 進行更智能的文本分割
        # 這個切割器會嘗試在段落、句子等自然界限處分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # 分隔優先級：段落 > 換行 > 句號 > 空格 > 字符
        )
        
        # 分割文本
        chunks = text_splitter.split_text(content)
        
        print(f"文件被分割為 {len(chunks)} 個重疊片段，使用 RecursiveCharacterTextSplitter")
        print(f"設定：分塊大小 = {chunk_size} 字符，重疊 = {chunk_overlap} 字符")
        
        # 對每個文本分塊生成嵌入向量
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # 跳過空的分塊
                response = ollama.embed(model=embedding_model, input=chunk) # 嵌入文本
                embeddings = response["embeddings"]
                
                # 儲存到 ChromaDB
                collection.add(
                    ids=[f"{os.path.basename(file_path)}-chunk-{i}"], # 使用文件名稱和索引作為 ID唯一識別碼
                    embeddings=embeddings,
                    documents=[chunk],
                    metadatas=[{
                        "source": file_path, 
                        "chunk_index": i,
                        "chunk_size": chunk_size,
                        "overlap": chunk_overlap
                    }]
                )
        return True
    except Exception as e:
        print(f"嵌入文件時出錯: {e}")
        return False

# 查詢處理
def query_database(prompt, top_k=3):
    try:
        # 生成查詢嵌入向量
        response = ollama.embed(model=embedding_model, input=prompt)
        
        # 從 ChromaDB 檢索
        results = collection.query(
            query_embeddings=response["embeddings"],
            n_results=top_k
        )
        
        # 組合檢索結果
        context = "\n".join(results['documents'][0])
        
        # 生成最終回應
        prompt=f"""
            基於以下內容：
                        
            {context}

            問題：{prompt}

            請根據上述內容提供準確的回答。如果上述內容無法回答問題，請誠實說明，不可以虛假編造回答。
            """
        output = ollama.generate(
            model=genrenator_model,
            prompt=prompt
        )
        return {
            "response": output['response'],
            "sources": [{"text": doc, "metadata": meta} 
                       for doc, meta in zip(results['documents'][0], results['metadatas'][0])]
        }
    except Exception as e:
        print(f"查詢處理時出錯: {e}")
        return {"error": str(e)}



# 指定文件路徑
file_path = "data/道路交通管理處罰條例.pdf"  # 替換為實際文件路徑

# 嵌入文件
if embed_document(file_path):
    print(f"文件 {file_path} 嵌入成功")
else:
    print("文件嵌入失敗")

# 測試查詢
while True:
    query = input("\n請輸入問題 (輸入'exit'退出): ")
    if query.lower() == 'exit':
        break
    
    result = query_database(query)
    if "error" in result:
        print(f"查詢錯誤: {result['error']}")
    else:
        print("\n回答:")
        print(result["response"])
        print("\n來源:")
        for i, source in enumerate(result["sources"]):
            print(f"來源 {i+1}:")
            print(f"文本: {source['text'][:150]}...")
            print(f"元數據: {source['metadata']}\n")