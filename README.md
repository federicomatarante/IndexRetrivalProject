# Index Retreival Project 🇮🇹 / 🇬🇧

## 🇮🇹 Italiano

**Disclaimer**: applicazione fatta per l'esame di _Gestione dell'informazione_, nel terzo anno della facoltà triennale di _Ingegneria Informatica_ di _UniMoRe_.  

_Index Retreival Project_ è un programma di recupero di documenti basato sul linguaggio naturale.
In particolare, i documenti utilizzati sono delle recensioni amazon dal dataset <a href="https://data.world/promptcloud/amazon-mobile-phone-reviews">Amazon Mobile Phone Reviews</a>.

Tra le varie funzioni, l'app permette di:
- Cercare tra le recensioni di smartphone utilizzando un linguaggio di query basato sul linguaggio naturale e operatori logici ( OR, AND, NOT ).
<div align="center">
  <img src="resources/normal_search.png" width="400"/>
</div>
- Avere la possibilità di filtrare i risultati per sentimento della recensione ( calcolato automaticamente tramite un modello di AI ).
<div align="center">
  <img src="resources/filter_serach.png" width="400"/>
</div>

Per maggiori informazioni leggere la presentazione nella repository.

### 🛠 Tecnologie usate
- Python: codice di base.
- Python/nltk: per il text preprocessing per la creazione dell'indice.
- Python/ReviewsHuggingFaceAnalyzer: per il transformer per il sentiment analysis.

---

## 🇬🇧 English

**Disclaimer**: This application was developed for the _Information Management_ exam, in the third year of the Bachelor's degree in _Computer Engineering_ at _UniMoRe_ (University of Modena and Reggio Emilia).  

_Index Retrieval Project_ is a document retrieval system based on natural language.  
Specifically, the documents used are Amazon reviews from the [Amazon Mobile Phone Reviews](https://data.world/promptcloud/amazon-mobile-phone-reviews) dataset.

Among its main features, the app allows users to:
- Search through smartphone reviews using a query language based on natural language and logical operators (OR, AND, NOT).
<div align="center">
  <img src="resources/normal_search.png" width="400"/>
</div>
- Filter search results by the sentiment of the review (automatically calculated using an AI model).
<div align="center">
  <img src="resources/filter_serach.png" width="400"/>
</div>

For more details, see the presentation available in the repository.

### 🛠 Technologies used
- Python: core implementation.
- Python/nltk: for text preprocessing and index creation.
- Python/ReviewsHuggingFaceAnalyzer: for the transformer-based sentiment analysis.
