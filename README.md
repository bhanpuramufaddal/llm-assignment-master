## RAG With Gemma

This is an app that takes an input, a pdf and a query, and generates answer for the query based on the input in the pdf.
<img width="800" alt="Screenshot 2024-03-21 at 10 00 05 AM" src="https://github.com/bhanpuramufaddal/llm-assignment-master/assets/46320499/dca3248f-5042-4da0-9832-333f896982af">

The structure of the app is as follows:
1. Backend -> Fastapi
2. Frontend -> Vue.js
3. Model -> gemma-2b-it (local)
4. VectorDB -> ChromaDb (local)   

The app is dockerized. I have created 2 separated containers for frontend and backend and orchestrated them using docker-compose.yaml file. 
In order to run the application:
1. `git clone https://github.com/bhanpuramufaddal/llm-assignment-master.git`
2. `cd llm-assignment-master`
3. `docker-compose build`
4. `docker-compose up -d`

### Now start the backend server.
1. `docker exec -it doc_qa_fastapi /bin/bash`
2. `uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload`

### Start the frontend server
1. `yarn install`
2. `yarn serve`

## Additional Notes
1. Only pdf files are supported.
2. The max file size supported is 10 MB.

Currently, the pdf files and subsequently vectordb index does not persist be aoptween concurrent api calls, this needs to be fixed. In order to fix that, we need to implweemnt sessions and additional methods such as:
1. create_index
2. upsert_file
3. remove_index

   



