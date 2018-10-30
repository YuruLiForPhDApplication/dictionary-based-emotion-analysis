# dictionary-based-emotion-analysis

The dictionary based approach assigns an emotion to each word in a text based on dictionaries of positive and negative words. 
First, read into the document of the politicians’ speeches and preprocess the text, including filtering numbers, punctuations, stop words, changing cases and extracting stem words. 

Next, import the emotional dictionary to mark the data including positive and negative tags and set the parameter to "named entitied unmodifiable". Then the preprocessed text is transformed into word bag and the word frequency is counted by TF node. In order to facilitate the statistics of word frequency, convert tags into strings. At this point, a document's emotional value is obtained by accumulating the frequency of emotional words in the document. This process is accomplished through the Pivoting node. 

After that, each document corresponds to a positive emotional word frequency and a negative emotional word frequency. The emotional attributes of the document also require a comparison of the frequency of the two types of emotional words. Emotion score is then calculated for each document as: (number of positive words - number of negative words) / total number of words. If the calculated value is positive, the emotional attribute of the text is positive, and vice versa. Artificially labeled text emotion attribute data are added to cross-check the accuracy of the evaluation model with the estimated values.

Note: The following diagram is only a sketch of the workflow produced with KNIME, and the specific analysis requires Python to write the relevant code. Syntactic dependency analysis and emotional level analysis need to be implemented in Python code. There are no relevant nodes in the schematic diagram. 
