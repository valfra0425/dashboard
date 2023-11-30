from textblob import TextBlob

texto = ("Very sad! According to the @zefogareiro, due to the entire Botafogo situation in the Brasileirão, ac "
         "Botafoguense in the interior of Bahia had a heart attack and, unfortunately, did not survive. May he rest in "
         "peace and may God comfort the hearts of his family and friends.")

analise = TextBlob(texto)

polaridade = analise.sentiment.polarity

print(polaridade)
