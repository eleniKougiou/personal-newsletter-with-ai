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


TLDR_PROMPT = """You are writing the opening of a personal daily newsletter.

Below are the sections of today's newsletter, each covering a different topic of interest.

Write a short, engaging TL;DR (3-5 sentences max) that captures the most important or interesting things happening today across all topics. Write it like a smart friend giving you the highlights before you dive in.

Sections:
{sections}"""


TAKEAWAY_PROMPT = """You are writing the closing of a personal daily newsletter.

Below are the sections of today's newsletter, each covering a different topic of interest.

Write a short closing thought, takeaway or reflection (2-3 sentences) that ties the day's news together. End with a relevant quote if one comes to mind naturally.

Sections:
{sections}"""