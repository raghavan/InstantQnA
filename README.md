# InstantQnA
Introducing the Instant QnA builder - a powerful tool that allows you to quickly and easily create searchable QnA systems from PDF files. Using state-of-the-art OpenAI technology, this tool generates search embeddings for your documents, making it easy to find the information you need. 

### How it works ?

1. Install the project's dependencies:   

   Windows:
   ```
   pip install -r requirements.txt
   ```
   Unix:
   ```
   python3 -m pip install -r requirements.txt
   ```

2. Update ```constants.py```, with your [OpenAI API Token]([https://beta.openai.com/account/api-keys])
   ```python
   token="<YOUR-OPENAI-API-TOKEN>"
   ```   

3. Place PDFs that you want to search inside ```/sources``` directory

4. Run the program

   Windows:
   ```bash
   python main.py
   ```
   Unix:
   ```bash
   python3 main.py
   ```

    An estimated cost to embed all of the files will be prompted for y/n. Choose `y` to proceed further.
    By default this engine use `text-embedding-ada-002` which is less expensive and also perfomant. You can update
    the code to embed using other models like davinci, etc...

5.  Once all of the files are full processed and embedded, then the program will show a prompt for you to enter your search query, if there are matching results it will return top 3 results with their score and source file name.

## Usage


If you have PDF files from which you want to build a question and answer engine, this tool should be useful for you. 

## Upload PDF file

To begin, select the PDF file that you want to create a QnA system for and upload it to the tool.

### ```read_source.py```
This python file reads all of the PDFs file from  ```/sources``` and then write all of its text content to ```/ai_generated/dumps```.

### ```get_file_data.py```
  Go through all files in ```sources``` and collect which file that hasn't been embedded yet, or the embedding has expired.


## Generate search embeddings

Once the file is uploaded, generate search embeddings for the contents of the PDF. This process may take a few minutes, depending on the size of the file.

### ```create_dataset.py```
Parses through all text content within a PDF, grouping them into coherent paragraphs no longer than 1000 tokens. This dataset is then saved in a CSV format, providing a structured and readable format for an AI model to process.

### ```embed.py```
  This file creates the text embedding using OpenAI Ada model (you can customize to any model) and also provides the search/query functions


## Execute search queries
You can now execute search queries to find the information you need. Enter your query in the search box and the tool will return any matching results from the PDF.

### ```main.py```
  The main function where you run the project
