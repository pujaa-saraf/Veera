import fitz  # PyMuPDF
import requests
import logging
import requests
from bs4 import BeautifulSoup

def google_search(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def lowercase(x):
  try:
    return x.lower()
  except Exception:
    return ""
def RemoveNonAscii(ini_string):
  result = ini_string.encode().decode('ascii', 'replace').replace(u'\ufffd', '')
  return result
def preprocessText(text):
  #do lower case
  Lowered_text=lowercase(text)
  #remove if a line contains less than 20 chars with less than 3 words
  #Splitted_Text=Lowered_text.split('\n')
  #for line in Splitted_Text:
  #  if len(line)<20 or len(line.split())<4:
  #    return ""
  #remove non ascii chars
  Cleaned=RemoveNonAscii(Lowered_text)
  return Cleaned
def parse_pdf_from_url(pdf_url):
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            pdf_bytes = response.content
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            # Extract text from each page
            pdf_text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                pdf_text += page.get_text()
            pdf_document.close()
        else:
            pdf_text = ''
    except Exception:
        logging.error(f"{pdf_url}")
        pdf_text = ''
    return pdf_text


def Data_Scraping(search_query,input_parms):
  #print(results)
  try:
    QueryAnsDict={}
    ParsedDocDict={}
    result_array=[]
    QueryAnsDict["search_query"]=search_query
    QueryAnsDict["parsed_documents"]=[]
    for result in input_parms:
      print(result)
      HighlightedText=result.snippet
      text_array=""
      HighlightedPara=""
      ParsedDocDict={}
      #print("Next: "+result)
      #eliminate youtube results, shopping results etc
      if result.link.find("youtube")>=0:
        continue
      if result.link.find(".pdf")>=0:
        #check domain and skip other than .com
        #print(parse_pdf_from_url(result))
        PDFDataCleaned=preprocessText(parse_pdf_from_url(result.link))
        #print(parse_pdf_from_url(result))
        #print(PDFDataCleaned)
        if len(PDFDataCleaned.strip())!=0:
          text_array=PDFDataCleaned
        #break
      else:
        soup=google_search(result.link)
        paragraphs = soup.find_all('p')
        all_para=[]
      # Print the text of each paragraph
        for paragraph in paragraphs:
          if HighlightedText in paragraph.text:
            HighlightedPara=paragraph.text
          all_para.append(preprocessText(paragraph.text))
        ParaJoined=' '.join(all_para)
        if len(ParaJoined.strip())!=0:
          text_array=ParaJoined
        #print("search res: ",len(text_array))
      #print(result)
      #print(text_array)
      #print(HighlightedText)
      #print(HighlightedPara)
      ParsedDocDict["url"]=result.link
      ParsedDocDict["full_document"]=text_array 
      ParsedDocDict["highlighted_text"]=HighlightedText
      ParsedDocDict["highlighted_paragraph"]=HighlightedPara
      #print(ParsedDocDict)
      QueryAnsDict["parsed_documents"].append(ParsedDocDict)
  except Exception:
     import logging
     logging.exception("traceback...")
    #print(QueryAnsDict)
    #print(QueryAnsDict["parsed_documents"][0].keys())
    #print(QueryAnsDict.keys())
  #print(QueryAnsDict["parsed_documents"][1]["highlighted_paragraph"])
  #print(QueryAnsDict["parsed_documents"][0]["highlighted_paragraph"])
  #print(len(QueryAnsDict["parsed_documents"][0]["full_document"]))
  #print(len(QueryAnsDict["parsed_documents"][1]["full_document"]))
  #print(QueryAnsDict["parsed_documents"][1]["url"])
  #print(QueryAnsDict["parsed_documents"][0]["url"])
  return QueryAnsDict