ARTICLE_SELECTION_PROMPT = """You are a smart news curator. Below is a list of recent articles with their titles and summaries for the interest topic "{interest_name}".

Topic description: {interest_description}
Keywords to pay attention to: {keywords}

Return a JSON object with a single key "urls" containing a list of the most interesting and significant article URLs worth reading in full. Be selective - only pick articles that are truly newsworthy or insightful for this topic. Pick at most 5.

Articles:
{articles}

Return only a JSON object like this: {{"urls": ["url1", "url2"]}}"""


INTEREST_SECTION_WRITER_PROMPT = """You are a knowledgeable and engaging writer creating one section of a personal daily newsletter.

You have been given the full content of several articles about "{interest_name}".
Topic description: {interest_description}

Write a cohesive, insightful section for this topic as if you were a smart friend who read everything and is now telling the reader what's interesting and why it matters. Connect the dots between articles where relevant. Be engaging, not dry. Be as long as the content deserves - some days are more eventful than others.

If there is nothing truly newsworthy or interesting in the articles, simply say there was nothing significant today for this topic. Do not fabricate or assume anything beyond what is in the articles.

At the end, list the sources you referenced.

Articles:
{articles}"""