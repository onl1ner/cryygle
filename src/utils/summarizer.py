from transformers import pipeline

class Summarizer:
    CHUNK_SIZE = 300

    def __init__(self, article):
        self.article = article
        self.summarizer = pipeline("summarization")

        pass

    def __chunkify(self):
        self.article = self.article.replace('.', '.<eos>')
        self.article = self.article.replace('?', '?<eos>')
        self.article = self.article.replace('!', '!<eos>')

        sentences = self.article.split('<eos>')

        chunks = []
        curr_chunk = 0

        for sentence in sentences:
            if len(chunks) == curr_chunk + 1:
                if len(chunks[curr_chunk]) + len(sentence.split(' ')) <= self.CHUNK_SIZE:
                    chunks[curr_chunk].extend(sentence.split(' '))
                else:
                    chunks.append(sentence.split(' '))
                    curr_chunk += 1
            else:
                chunks.append(sentence.split(' '))
        
        for i in range(len(chunks)):
            chunks[i] = ' '.join(chunks[i])
        
        return chunks

    def summarize(self):
        chunks = self.__chunkify()
        result = self.summarizer(chunks, max_length=120, min_length=30, do_sample=False)

        return ' '.join([summ['summary_text'] for summ in result])

    pass