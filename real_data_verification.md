# 50-company real-data verification — 2026-10-24

Source: https://huggingface.co/datasets/datahiveai/ycombinator-companies (yc-companies.csv). Downloaded with curl; parsed with Python standard-library csv. No dataset package was added. ChromaDB 1.5.9; existing ONNX Runtime 1.20.1. Raw CSV and raw JSON results are ignored under data/; chroma_store/ remains ignored.

CSV SHA-256: `6dd6fddcfbf93e31267a3bab720db81235e3bb13ec43ef7a0e57cfe96e59d24a`.

## Actual structure

5384 rows; 77 fields. All Company ID values are present and unique.

- `Company ID`
- `Company Name`
- `Slug`
- `One Liner`
- `Long Description`
- `Website`
- `Location`
- `All Locations`
- `City`
- `Country`
- `City Tag`
- `Regions`
- `Team Size`
- `Year Founded`
- `Launched At`
- `Batch`
- `Batch Name`
- `Stage`
- `Status`
- `YC DC Status`
- `YC DC Company URL`
- `Industry`
- `Subindustry`
- `Industries`
- `Tags`
- `Tags Highlighted`
- `Is Hiring`
- `Nonprofit`
- `Top Company`
- `Former Names`
- `Object ID`
- `Logo URL`
- `Twitter URL`
- `LinkedIn URL`
- `GitHub URL`
- `Facebook URL`
- `CB URL`
- `Primary Group Partner`
- `Question Answers`
- `Founders Count`
- `founderAvatarFilePaths`
- `Founder 1 Name`
- `Founder 1 Title`
- `Founder 1 Bio`
- `Founder 1 Twitter URL`
- `Founder 1 LinkedIn URL`
- `Founder 1 Avatar URL`
- `Founder 2 Name`
- `Founder 2 Title`
- `Founder 2 Bio`
- `Founder 2 Twitter URL`
- `Founder 2 LinkedIn URL`
- `Founder 2 Avatar URL`
- `Founder 3 Name`
- `Founder 3 Title`
- `Founder 3 Bio`
- `Founder 3 Twitter URL`
- `Founder 3 LinkedIn URL`
- `Founder 3 Avatar URL`
- `Founder 4 Name`
- `Founder 4 Title`
- `Founder 4 Bio`
- `Founder 4 Twitter URL`
- `Founder 4 LinkedIn URL`
- `Founder 4 Avatar URL`
- `Founder 5 Name`
- `Founder 5 Title`
- `Founder 5 Bio`
- `Founder 5 Twitter URL`
- `Founder 5 LinkedIn URL`
- `Founder 5 Avatar URL`
- `Founder 6 Name`
- `Founder 6 Title`
- `Founder 6 Bio`
- `Founder 6 Twitter URL`
- `Founder 6 LinkedIn URL`
- `Founder 6 Avatar URL`

## Description lengths and missing values

Character lengths below exclude empty values. Empty CSV values are treated as missing. A filled value is not necessarily informative.

| Field | Missing | Median characters | 90th percentile | Maximum |
|---|---:|---:|---:|---:|

| One Liner | 153 | 48 | 68 | 70 |

| Long Description | 356 | 378.0 | 951 | 6034 |

| Tags | 547 | 31 | 61 | 104 |

| Company Name | 0 | 8.0 | 13 | 44 |

| Company ID | 0 | 5.0 | 5 | 5 |

| Industry | 0 | 7.0 | 10 | 28 |

| Subindustry | 0 | 21.0 | 38 | 55 |

| Batch | 0 | 11.0 | 11 | 11 |

| Status | 0 | 6.0 | 8 | 8 |

| YC DC Company URL | 0 | 19.0 | 24 | 53 |

## Five representative rows

Rows at positions 0, 1346, 2692, 4038, and 5383 (zero-based), spread across the alphabetically ordered CSV. These illustrate structure; they are not the 50-record selection.

| Company (ID) | Description summary | Industry | Batch | Status |
|---|---|---|---|---|

| 1000Memories (192) | Organizes and shares old photos, memories, and family trees. | Consumer | Summer 2010 | Acquired |

| Duranium (30781) | Produces critical metals in the US using a proposed lower-cost process. | Industrials | Summer 2025 | Active |

| Mailgun (162) | Email delivery, receipt, and tracking through a developer API. | B2B | Winter 2011 | Acquired |

| Safely Finance (12461) | Pay-over-time financing embedded in rental and moving workflows. | Consumer | Summer 2019 | Inactive |

| Zyper (1841) | Helps brands find and engage advocates within their social following. | B2B | Winter 2018 | Acquired |

## Item definition and loading policy

One item is one company, with stable ID yc:<Company ID>. Embed One Liner, Tags, and Long Description, in that order. Company name is metadata only, except where the original company-written description itself mentions the name. Short summaries and tags lead so the main concept survives a long description.

Metadata mapping: {"company_name": "Company Name", "company_id": "Company ID", "industry": "Industry", "subindustry": "Subindustry", "batch": "Batch", "status": "Status", "yc_url": "YC DC Company URL"}. YC URL paths are expanded with https://www.ycombinator.com; empty metadata values are omitted.

Select the first 50 usable companies after a deterministic shuffle with seed 42, independent of query results. Require a company ID and at least 40 descriptive characters and 8 words from One Liner + Long Description; tags alone cannot qualify a row. This is a small sample, not representative coverage of all startup concepts.

The installed default MiniLM embedding model uses a 256-token input limit. Five selected combined documents exceeded it. The loader retains the leading text that fits within 256 tokens including special tokens, and stores that exact text in Chroma. It does not split companies into multiple items. The full original descriptions remain in the raw CSV. Long marketing passages and founder history may dilute retrieval; a future text-selection policy may help, but was not built here.

## Measured load and restart

| Metric | First successful load | Second process |
|---|---:|---:|

| Rows inspected | 54 | 54 |

| Selected | 50 | 50 |

| Collection before | 0 | 50 |

| Inserted | 50 | 0 |

| Collection after | 50 | 50 |

| Unique IDs | 50 | 50 |

| Unique documents | 50 | 50 |

| Original smoke collection count | 10 | 10 |

| Embedding + insertion seconds | 2.0418917920906097 | 2.0815059542655945e-07 |

| Total load setup + insertion seconds | 2.637589040910825 | 0.08075641607865691 |

Skipped 4 rows: {'insufficient_description': 4}. All 50 new records were passed to collection.add() together in one batch. Existing IDs are checked before insertion. The second process added zero records and returned identical query results. The 10-record startup_ideas collection was preserved.

Embedding/insertion time per item: 0.04083783584181219 seconds. Total loading time includes tokenizer/client setup and ID checks, but excludes CSV download, parsing/selection and the subsequent searches. No embedding-model download was needed in this stage.

Simple linear projections from measured batch embedding/insertion time: 500 items ≈ 20.42 seconds; 1,000 ≈ 40.84 seconds. These are rough warm-model estimates, not measurements; longer inputs, hardware load, batch sizes and indexing can change them.

## Query interpretation

Study focus: Eduflow is related to student engagement and online learning, but its document does not describe distraction detection or rewards. The remaining results mostly overlap in education or social-media vocabulary.

Food waste: neither food query produced a close pantry-based meal-planning match. Cowlar concerns dairy herd monitoring; No Lean Season concerns seasonal hunger; Voiceops concerns customer conversations. These are not successful matches to the product concept.

Meeting follow-up: Voiceops is partially relevant because it analyzes recorded customer conversations. Its document does not promise meeting-to-task conversion. Contour handles banking conversations; AutoComputer automates computer tasks. No exact meeting follow-up tool is demonstrated.

Original Test 1 and Test 2 remain useful unmet-coverage probes, but neither is a demonstrated semantic-match success against these 50 companies. The synthetic expected documents are absent. Final README positive tests may need revision after inspecting a broader authorized corpus; no final query replacement has been selected.

Top distances: study focus 0.9762965440750122, meeting follow-up 1.18593168258667, food waste 1.3142731189727783, original Test 1 1.0854973793029785, original Test 2 1.455267310142517. Nonsense neighbors range from 1.8978135585784912 to 1.968353033065796. Nonsense distances were higher here, but a low distance can still represent a weak concept match. No clearly exact product match was found for the requested queries. No threshold, percentage, or originality formula is established.

## Complete raw search results

All results below show the exact stored document and metadata returned by Chroma. Distance uses the unchanged default squared L2 setup; lower is closer. Both processes produced identical results.

### Study focus

A tool that notices when students get distracted online while studying and rewards them for staying focused.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Eduflow | yc:1674 | 0.9762965440750122 |

| 2 | Skill-lync | yc:12234 | 1.3278632164001465 |

| 3 | Lumona | yc:29459 | 1.4588732719421387 |

| 4 | Prendea | yc:23278 | 1.4829506874084473 |

| 5 | Extern | yc:1462 | 1.484943151473999 |

#### Rank 1: Eduflow

Document:

Summary: Create and run collaborative online learning experiences.
Tags: education; elearning
Description: Eduflow is a tool for running active online learning experiences. We are used at thousands of institutions around the world all the way from middle school to corporate training at Google. We believe that digital tools for learning need to be more than just a playlist of videos. We're building learning activities that instructors can use to engage learners and make them active participants in their own learning process.

Metadata:

```json
{
  "company_name": "Eduflow",
  "company_id": "1674",
  "industry": "Education",
  "subindustry": "Education",
  "batch": "Summer 2017",
  "yc_url": "https://www.ycombinator.com/companies/eduflow",
  "status": "Acquired"
}
```

#### Rank 2: Skill-lync

Document:

Summary: Online engineering college for India. Learn technical skills & get…
Tags: education; income-share-agreements; elearning
Description: Skill-Lync provides job leading engineering education online. We started with a special focus in Mechanical, Electrical, Electronics, Civil & Computer Science engineering and have become one of the world's leading & highest rated platforms in teaching high-end technical skills that help students get a job.

Metadata:

```json
{
  "status": "Active",
  "subindustry": "Education",
  "company_id": "12234",
  "company_name": "Skill-lync",
  "yc_url": "https://www.ycombinator.com/companies/skill-lync",
  "industry": "Education",
  "batch": "Winter 2019"
}
```

#### Rank 3: Lumona

Document:

Summary: AI-enabled search engine featuring insights from social media.
Tags: artificial-intelligence; generative-ai; consumer; search
Description: Lumona is an AI-enabled search engine featuring insights from social media. When you’re looking to buy a new phone, instead of adding reddit to the end of your search and opening tabs of threads that take forever to get through, you can search on Lumona to get all of that processed for you on one page so you can make the best decision while saving time.

Metadata:

```json
{
  "status": "Active",
  "batch": "Winter 2024",
  "industry": "Consumer",
  "subindustry": "Consumer",
  "yc_url": "https://www.ycombinator.com/companies/lumona",
  "company_name": "Lumona",
  "company_id": "29459"
}
```

#### Rank 4: Prendea

Document:

Summary: Live afterschool classes for Spanish-speaking kids ages 4 to 15.
Tags: education; elearning; subscriptions
Description: Prendea offers live afterschool classes to Spanish-speaking kids ages 4 to 15.  For a fixed monthly price, kids can choose as many classes as they like from our large selection that ranges from TikTok choreography to astronomy.

Metadata:

```json
{
  "batch": "Winter 2021",
  "subindustry": "Education",
  "status": "Inactive",
  "company_id": "23278",
  "company_name": "Prendea",
  "industry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/prendea"
}
```

#### Rank 5: Extern

Document:

Summary: Professional Experience Anytime, Anywhere.
Tags: education; marketplace; elearning; recruiting; remote-work
Description: At Extern, we’re solving the experience gap.  Extern created the remote Externship, a skill-building work experience that is easier for students to access, and easier for companies to run, than an internship.  Our mission is to help anyone discover and launch their career through professional experiences available anywhere at any time.  Since 2020, we’ve created and powered Externships for over 50,000 students on behalf of companies from Fortune 500s to startups.  

After spending $100K on average for a 4-year degree, graduates find that almost 40% of entry level jobs on Linkedin required 3+ years of work experience. Internships are how many college students get this kind of experience, but the demand for good internships outstrips the supply. Internship programs are difficult to scale, they favor students who already have social capital, and they’re time-consuming for employers to run.

Externships are short, online, project-based work experiences that employers can offer to hundreds of students using less resource and employee time than it would take to support an intern.  Extern makes the complex process

Metadata:

```json
{
  "company_id": "1462",
  "yc_url": "https://www.ycombinator.com/companies/extern",
  "industry": "Consumer",
  "company_name": "Extern",
  "batch": "Winter 2017",
  "subindustry": "Education",
  "status": "Active"
}
```

### Food waste

An app that looks at food someone already has at home and suggests meals so it doesn't get wasted.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Cowlar | yc:1445 | 1.3142731189727783 |

| 2 | No Lean Season | yc:1553 | 1.37705397605896 |

| 3 | Belvo | yc:13610 | 1.4308130741119385 |

| 4 | Uberduck | yc:25117 | 1.443100929260254 |

| 5 | Abhi | yc:24685 | 1.4626660346984863 |

#### Rank 1: Cowlar

Document:

Summary: Fitbit for dairy cows. Farms use cowlar's alerts & recommendations to…
Tags: machine-learning; iot; agriculture
Description: Cowlar, a fitbit for dairy cows provides data as a service to help dairy producers optimize operations and improve herd health.

It's simple. You strap it around a cow's neck. It measures temperature, activity and cow behavior. Cowlar makes sense of the data and sends the farmers actionable recommendations on how to:

1. Boost reproduction rates
2. Identify diseases instantly
3. Improve milk yield 
4. We can even tell if someone is stealing your cow ! 

Cowlar is simple, affordable and easy to use. It's rugged, water proof, comes with a 6 Month battery life so farmers dont have to worry about charging and farmers can be sent text messages in any language/ for those who cant read, we can send an automated phone call.

Metadata:

```json
{
  "company_id": "1445",
  "status": "Inactive",
  "subindustry": "Industrials -> Agriculture",
  "company_name": "Cowlar",
  "yc_url": "https://www.ycombinator.com/companies/cowlar",
  "industry": "Industrials",
  "batch": "Winter 2017"
}
```

#### Rank 2: No Lean Season

Document:

Summary: A bus ticket out of poverty
Tags: nonprofit
Description: No Lean Season reduces the negative effects of seasonality on the poorest in rural agricultural areas by enabling labor mobility that increases incomes. It is a new program that they are testing in Evidence Action Beta's portfolio, based on rigorous experimental evidence.

They give a travel subsidy of $20 to very poor rural laborers so they can send a family member to a nearby city to find a job during the period between planting and harvesting. This is the time in rural areas when there are no jobs, no income, and when families miss meals. This seasonal poverty affects 600 million people around the world.

With a temporary job during this 'lean season,' households are are able to put an additional meal on the table for every member of the family each and every day. That’s 500 additional meals during the lean season.

Metadata:

```json
{
  "batch": "Winter 2017",
  "company_id": "1553",
  "status": "Inactive",
  "yc_url": "https://www.ycombinator.com/companies/no-lean-season",
  "industry": "Unspecified",
  "subindustry": "Unspecified",
  "company_name": "No Lean Season"
}
```

#### Rank 3: Belvo

Document:

Summary: Open Finance API platform for Latam.
Tags: fintech; saas
Description: We are Belvo, a financial API platform for Latam that enables any company or developer to access and interpret their end-users' financial information, through one easy-to-use API. Think Plaid for Latam.

Our vision is to power the next generation of financial services in Latam by enabling more inclusive, efficient and empowering offerings through tech and data. Latam is a very exciting and dynamic place to be right now and a great place to build infrastructure for the next generation of financial products for a huge market.

Metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/belvo",
  "industry": "Fintech",
  "company_name": "Belvo",
  "batch": "Winter 2020",
  "company_id": "13610",
  "status": "Active",
  "subindustry": "Fintech -> Banking and Exchange"
}
```

#### Rank 4: Uberduck

Document:

Summary: Fast, professional content creation with AI audio, image, and video.
Description: Uberduck makes tools high-quality audiovisual content creation tools for product companies, brands, agencies, and musicians.

We offer audio generation, image generation, and video generation functionality, including enterprise workflow APIs to power end-to-end video creation experiences.

Vocal samples and full songs produced by our text-to-speech, text-to-singing, text-to-rapping, lyric video generation, and voice conversion technologies power:
- AI remixes and original songs for musicians ranging from hobbyists to the largest DJs in the world.
- Personalized musical content in marketing campaigns.
- A variety of music-related consumer experiences built on top of our APIs.

Metadata:

```json
{
  "status": "Active",
  "company_name": "Uberduck",
  "industry": "B2B",
  "batch": "Winter 2022",
  "subindustry": "B2B -> Marketing",
  "company_id": "25117",
  "yc_url": "https://www.ycombinator.com/companies/uberduck"
}
```

#### Rank 5: Abhi

Document:

Summary: Abhi is Pakistan's 1st financial wellness platform focusing on…
Tags: fintech
Description: An early wage access platform allowing salaried employees to draw down a percentage of their accrued salary before the next payroll cycle. Helping employees to avoid late payment fee on bills, access emergency cash and substitute expensive debt. We work on a B2B2C model allowing companies to extend the product as a benefits program to their employee base.

Metadata:

```json
{
  "company_name": "Abhi",
  "yc_url": "https://www.ycombinator.com/companies/abhi",
  "status": "Active",
  "batch": "Summer 2021",
  "subindustry": "Fintech -> Credit and Lending",
  "company_id": "24685",
  "industry": "Fintech"
}
```

### Meeting follow-up

Software that listens to meetings and automatically turns conversations into organized follow-up tasks.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Voiceops | yc:1438 | 1.18593168258667 |

| 2 | Contour | yc:28816 | 1.2166919708251953 |

| 3 | Uberduck | yc:25117 | 1.3440475463867188 |

| 4 | AutoComputer | yc:30077 | 1.3562157154083252 |

| 5 | Eduflow | yc:1674 | 1.3830647468566895 |

#### Rank 1: Voiceops

Document:

Summary: We help B2C companies learn from every customer interaction
Tags: artificial-intelligence; analytics
Description: The richest data source about customers — their conversations — is the least accessible. Their mission is to provide easy access to customer conversations, and make voice data queryable. Their product analyzes the content of sales and support conversations and generates insights on phrases that maximize successful outcomes.

Metadata:

```json
{
  "batch": "Winter 2017",
  "company_id": "1438",
  "subindustry": "B2B -> Sales",
  "yc_url": "https://www.ycombinator.com/companies/voiceops",
  "status": "Active",
  "industry": "B2B",
  "company_name": "Voiceops"
}
```

#### Rank 2: Contour

Document:

Summary: Voice AI for Financial Institutions
Tags: generative-ai; b2b; workflow-automation; enterprise-software
Description: Contour is a voice AI platform for financial institutions. It handles voice and chat conversations for collections and support with deep banking knowledge and built-in compliance guardrails.

Metadata:

```json
{
  "batch": "Summer 2023",
  "status": "Active",
  "industry": "B2B",
  "company_id": "28816",
  "subindustry": "B2B",
  "yc_url": "https://www.ycombinator.com/companies/contour",
  "company_name": "Contour"
}
```

#### Rank 3: Uberduck

Document:

Summary: Fast, professional content creation with AI audio, image, and video.
Description: Uberduck makes tools high-quality audiovisual content creation tools for product companies, brands, agencies, and musicians.

We offer audio generation, image generation, and video generation functionality, including enterprise workflow APIs to power end-to-end video creation experiences.

Vocal samples and full songs produced by our text-to-speech, text-to-singing, text-to-rapping, lyric video generation, and voice conversion technologies power:
- AI remixes and original songs for musicians ranging from hobbyists to the largest DJs in the world.
- Personalized musical content in marketing campaigns.
- A variety of music-related consumer experiences built on top of our APIs.

Metadata:

```json
{
  "status": "Active",
  "batch": "Winter 2022",
  "company_id": "25117",
  "subindustry": "B2B -> Marketing",
  "yc_url": "https://www.ycombinator.com/companies/uberduck",
  "industry": "B2B",
  "company_name": "Uberduck"
}
```

#### Rank 4: AutoComputer

Document:

Summary: Desktop RPA with AI computer use
Tags: deep-learning; b2b; enterprise; automation; ai
Description: AutoComputer is a desktop robotic process automation system.  Given just a text prompt, our AI automates tedious tasks such as financial data entry by performing all the clicks and keystrokes for you.

Metadata:

```json
{
  "company_id": "30077",
  "company_name": "AutoComputer",
  "batch": "Fall 2024",
  "yc_url": "https://www.ycombinator.com/companies/autocomputer",
  "industry": "B2B",
  "status": "Active",
  "subindustry": "Consumer"
}
```

#### Rank 5: Eduflow

Document:

Summary: Create and run collaborative online learning experiences.
Tags: education; elearning
Description: Eduflow is a tool for running active online learning experiences. We are used at thousands of institutions around the world all the way from middle school to corporate training at Google. We believe that digital tools for learning need to be more than just a playlist of videos. We're building learning activities that instructors can use to engage learners and make them active participants in their own learning process.

Metadata:

```json
{
  "company_name": "Eduflow",
  "company_id": "1674",
  "status": "Acquired",
  "batch": "Summer 2017",
  "industry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/eduflow",
  "subindustry": "Education"
}
```

### Semantic test 1

A tool that notices when college students drift to social media during homework and gives them a virtual pet for staying on task.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Eduflow | yc:1674 | 1.0854973793029785 |

| 2 | Skill-lync | yc:12234 | 1.3933361768722534 |

| 3 | Lumona | yc:29459 | 1.4268100261688232 |

| 4 | Extern | yc:1462 | 1.4594666957855225 |

| 5 | Prendea | yc:23278 | 1.5447111129760742 |

#### Rank 1: Eduflow

Document:

Summary: Create and run collaborative online learning experiences.
Tags: education; elearning
Description: Eduflow is a tool for running active online learning experiences. We are used at thousands of institutions around the world all the way from middle school to corporate training at Google. We believe that digital tools for learning need to be more than just a playlist of videos. We're building learning activities that instructors can use to engage learners and make them active participants in their own learning process.

Metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/eduflow",
  "company_name": "Eduflow",
  "company_id": "1674",
  "subindustry": "Education",
  "status": "Acquired",
  "industry": "Education",
  "batch": "Summer 2017"
}
```

#### Rank 2: Skill-lync

Document:

Summary: Online engineering college for India. Learn technical skills & get…
Tags: education; income-share-agreements; elearning
Description: Skill-Lync provides job leading engineering education online. We started with a special focus in Mechanical, Electrical, Electronics, Civil & Computer Science engineering and have become one of the world's leading & highest rated platforms in teaching high-end technical skills that help students get a job.

Metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/skill-lync",
  "company_id": "12234",
  "subindustry": "Education",
  "company_name": "Skill-lync",
  "batch": "Winter 2019",
  "industry": "Education",
  "status": "Active"
}
```

#### Rank 3: Lumona

Document:

Summary: AI-enabled search engine featuring insights from social media.
Tags: artificial-intelligence; generative-ai; consumer; search
Description: Lumona is an AI-enabled search engine featuring insights from social media. When you’re looking to buy a new phone, instead of adding reddit to the end of your search and opening tabs of threads that take forever to get through, you can search on Lumona to get all of that processed for you on one page so you can make the best decision while saving time.

Metadata:

```json
{
  "subindustry": "Consumer",
  "yc_url": "https://www.ycombinator.com/companies/lumona",
  "company_name": "Lumona",
  "batch": "Winter 2024",
  "company_id": "29459",
  "status": "Active",
  "industry": "Consumer"
}
```

#### Rank 4: Extern

Document:

Summary: Professional Experience Anytime, Anywhere.
Tags: education; marketplace; elearning; recruiting; remote-work
Description: At Extern, we’re solving the experience gap.  Extern created the remote Externship, a skill-building work experience that is easier for students to access, and easier for companies to run, than an internship.  Our mission is to help anyone discover and launch their career through professional experiences available anywhere at any time.  Since 2020, we’ve created and powered Externships for over 50,000 students on behalf of companies from Fortune 500s to startups.  

After spending $100K on average for a 4-year degree, graduates find that almost 40% of entry level jobs on Linkedin required 3+ years of work experience. Internships are how many college students get this kind of experience, but the demand for good internships outstrips the supply. Internship programs are difficult to scale, they favor students who already have social capital, and they’re time-consuming for employers to run.

Externships are short, online, project-based work experiences that employers can offer to hundreds of students using less resource and employee time than it would take to support an intern.  Extern makes the complex process

Metadata:

```json
{
  "batch": "Winter 2017",
  "subindustry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/extern",
  "industry": "Consumer",
  "status": "Active",
  "company_id": "1462",
  "company_name": "Extern"
}
```

#### Rank 5: Prendea

Document:

Summary: Live afterschool classes for Spanish-speaking kids ages 4 to 15.
Tags: education; elearning; subscriptions
Description: Prendea offers live afterschool classes to Spanish-speaking kids ages 4 to 15.  For a fixed monthly price, kids can choose as many classes as they like from our large selection that ranges from TikTok choreography to astronomy.

Metadata:

```json
{
  "company_name": "Prendea",
  "subindustry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/prendea",
  "industry": "Education",
  "batch": "Winter 2021",
  "company_id": "23278",
  "status": "Inactive"
}
```

### Semantic test 2

People describe what's sitting in their fridge and get dinner suggestions before their groceries go bad.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Voiceops | yc:1438 | 1.455267310142517 |

| 2 | No Lean Season | yc:1553 | 1.4723060131072998 |

| 3 | Modular Science | yc:1659 | 1.498821496963501 |

| 4 | Spoken | yc:24816 | 1.575698971748352 |

| 5 | Mendel | yc:23240 | 1.6137590408325195 |

#### Rank 1: Voiceops

Document:

Summary: We help B2C companies learn from every customer interaction
Tags: artificial-intelligence; analytics
Description: The richest data source about customers — their conversations — is the least accessible. Their mission is to provide easy access to customer conversations, and make voice data queryable. Their product analyzes the content of sales and support conversations and generates insights on phrases that maximize successful outcomes.

Metadata:

```json
{
  "company_id": "1438",
  "subindustry": "B2B -> Sales",
  "company_name": "Voiceops",
  "industry": "B2B",
  "status": "Active",
  "batch": "Winter 2017",
  "yc_url": "https://www.ycombinator.com/companies/voiceops"
}
```

#### Rank 2: No Lean Season

Document:

Summary: A bus ticket out of poverty
Tags: nonprofit
Description: No Lean Season reduces the negative effects of seasonality on the poorest in rural agricultural areas by enabling labor mobility that increases incomes. It is a new program that they are testing in Evidence Action Beta's portfolio, based on rigorous experimental evidence.

They give a travel subsidy of $20 to very poor rural laborers so they can send a family member to a nearby city to find a job during the period between planting and harvesting. This is the time in rural areas when there are no jobs, no income, and when families miss meals. This seasonal poverty affects 600 million people around the world.

With a temporary job during this 'lean season,' households are are able to put an additional meal on the table for every member of the family each and every day. That’s 500 additional meals during the lean season.

Metadata:

```json
{
  "batch": "Winter 2017",
  "subindustry": "Unspecified",
  "company_name": "No Lean Season",
  "status": "Inactive",
  "company_id": "1553",
  "yc_url": "https://www.ycombinator.com/companies/no-lean-season",
  "industry": "Unspecified"
}
```

#### Rank 3: Modular Science

Document:

Summary: We're making it easier to do sustainable farming.
Tags: agriculture

Metadata:

```json
{
  "company_name": "Modular Science",
  "company_id": "1659",
  "subindustry": "Industrials -> Agriculture",
  "industry": "Industrials",
  "batch": "Summer 2017",
  "status": "Inactive",
  "yc_url": "https://www.ycombinator.com/companies/modular-science"
}
```

#### Rank 4: Spoken

Document:

Summary: Never overpay online
Tags: artificial-intelligence; machine-learning; marketplace; consumer; e-commerce
Description: Spoken is a website where users compare buying options for the exact same product across multiple stores. We help our users never overpay online.

Dane is a two-time technical YC founder; he sold his previous company, Parklet, to Greenhouse where he was VP of Platform for 4.5 years. Geoff is a Stanford MBA grad and sold his previous company Cabrio Taxi.

Metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/spoken",
  "company_name": "Spoken",
  "industry": "Consumer",
  "batch": "Summer 2021",
  "company_id": "24816",
  "status": "Active",
  "subindustry": "Consumer -> Home and Personal"
}
```

#### Rank 5: Mendel

Document:

Summary: Workflows to empower employees to spend while finance stay in control
Tags: fintech; b2b

Metadata:

```json
{
  "batch": "Winter 2021",
  "status": "Active",
  "subindustry": "Fintech -> Banking and Exchange",
  "company_id": "23240",
  "yc_url": "https://www.ycombinator.com/companies/mendel",
  "company_name": "Mendel",
  "industry": "Fintech"
}
```

### Unrelated query

Quantum marshmallow nebula dances inside a purple theorem.

| Rank | Company | ID | Distance |
|---|---|---|---|

| 1 | Hyperbound | yc:28788 | 1.8978135585784912 |

| 2 | Belvo | yc:13610 | 1.9095304012298584 |

| 3 | XTraffic | yc:29956 | 1.9132198095321655 |

| 4 | Extern | yc:1462 | 1.934356927871704 |

| 5 | Omnistrate | yc:27813 | 1.968353033065796 |

#### Rank 1: Hyperbound

Document:

Summary: Sales call roleplay with realistic conversational AI buyers
Tags: ai-enhanced-learning; generative-ai; b2b; sales; sales-enablement
Description: Hyperbound is a simulated AI sales roleplay platform that turns ICP descriptions into interactive AI buyers in less than 2 minutes. It helps your sales team onboard 50% faster and boosts your team's conversions on cold, warm, & discovery calls.

Every sales team wants to do more roleplays, but it's often unscalable and biased. Instead of having your sellers practice on real prospects and burn leads in the process, Hyperbound allows your reps to get realistic at-bats with an AI buyer. Sellers can finally gain call confidence and mastery in a simulated environment that doesn't put your pipeline at risk and gives time back to your managers. 

Interested in trying it out today? Start a free demo simulation at https://app.hyperbound.ai/buyers?invite=bookface and contact us at founders@hyperbound.ai for next steps.

Metadata:

```json
{
  "subindustry": "B2B -> Sales",
  "yc_url": "https://www.ycombinator.com/companies/hyperbound",
  "status": "Active",
  "company_id": "28788",
  "industry": "B2B",
  "batch": "Summer 2023",
  "company_name": "Hyperbound"
}
```

#### Rank 2: Belvo

Document:

Summary: Open Finance API platform for Latam.
Tags: fintech; saas
Description: We are Belvo, a financial API platform for Latam that enables any company or developer to access and interpret their end-users' financial information, through one easy-to-use API. Think Plaid for Latam.

Our vision is to power the next generation of financial services in Latam by enabling more inclusive, efficient and empowering offerings through tech and data. Latam is a very exciting and dynamic place to be right now and a great place to build infrastructure for the next generation of financial products for a huge market.

Metadata:

```json
{
  "industry": "Fintech",
  "company_name": "Belvo",
  "yc_url": "https://www.ycombinator.com/companies/belvo",
  "company_id": "13610",
  "batch": "Winter 2020",
  "status": "Active",
  "subindustry": "Fintech -> Banking and Exchange"
}
```

#### Rank 3: XTraffic

Document:

Summary: Technology for cities to automate and manage their traffic lights.
Description: XTraffic is at the intersection of advancements in sensor technology and affordability. This means entire cities can affordably upgrade their infrastructure - and some already are. We are live in multiple cities, with both ongoing and successful pilots, corridors of multiple intersections, and soon to be entire cities. Our customers enjoy less traffic, better safety, and data on which to build their future.

Metadata:

```json
{
  "status": "Active",
  "subindustry": "Government",
  "company_name": "XTraffic",
  "batch": "Summer 2024",
  "yc_url": "https://www.ycombinator.com/companies/xtraffic",
  "industry": "Government",
  "company_id": "29956"
}
```

#### Rank 4: Extern

Document:

Summary: Professional Experience Anytime, Anywhere.
Tags: education; marketplace; elearning; recruiting; remote-work
Description: At Extern, we’re solving the experience gap.  Extern created the remote Externship, a skill-building work experience that is easier for students to access, and easier for companies to run, than an internship.  Our mission is to help anyone discover and launch their career through professional experiences available anywhere at any time.  Since 2020, we’ve created and powered Externships for over 50,000 students on behalf of companies from Fortune 500s to startups.  

After spending $100K on average for a 4-year degree, graduates find that almost 40% of entry level jobs on Linkedin required 3+ years of work experience. Internships are how many college students get this kind of experience, but the demand for good internships outstrips the supply. Internship programs are difficult to scale, they favor students who already have social capital, and they’re time-consuming for employers to run.

Externships are short, online, project-based work experiences that employers can offer to hundreds of students using less resource and employee time than it would take to support an intern.  Extern makes the complex process

Metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/extern",
  "company_id": "1462",
  "subindustry": "Education",
  "batch": "Winter 2017",
  "industry": "Consumer",
  "company_name": "Extern",
  "status": "Active"
}
```

#### Rank 5: Omnistrate

Document:

Summary: Transform any software to multi-cloud SaaS in minutes not years
Tags: developer-tools; saas; b2b; cloud-computing; infrastructure
Description: Omnistrate is a cloud platform to SaaS-ify your docker image in minutes instead of years.

Let’s say you have an open-source software, and you want to monetize your invention by building a multi-cloud SaaS solution. You can either spend years doing it yourself or use Omnistrate to do it in no time.

Get started today by simply importing your existing docker-compose.

Metadata:

```json
{
  "subindustry": "B2B",
  "industry": "B2B",
  "company_name": "Omnistrate",
  "yc_url": "https://www.ycombinator.com/companies/omnistrate",
  "batch": "Winter 2023",
  "status": "Active",
  "company_id": "27813"
}
```

## Problems and changes

No loader or query execution errors occurred. During dependency inspection, an attempted lookup of a nonexistent MAX_TOKENS class constant raised AttributeError; inspection of the installed source then confirmed max_tokens() returns 256. No dependency change was required. Missing text caused four selection skips; five overly long documents required explicit truncation.

Created load_yc.py and this verification report; updated .gitignore and appended the exact user prompt to prompt_log.md. app.py is unchanged. requirements.txt remains chromadb only; the loader uses Python standard-library modules and tokenizers already required by Chroma. No final app, README, threshold, full-corpus embedding, commit, or push was performed.
