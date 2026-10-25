# 1,000-company scaling verification — 2026-10-24

## Scope and provenance

Expanded the existing yc_startups collection in place using the same local data/yc-companies.csv from https://huggingface.co/datasets/datahiveai/ycombinator-companies. No new dataset download was needed. ChromaDB 1.5.9 and the existing default MiniLM embeddings were retained. No CLI, frontend, scoring, explanation feature, deployment, final README, commit or push was created.

## Selection, model and preservation

Kept the deterministic seed-42 shuffled order and expanded its first 50 usable rows to its first 1,000 usable rows. A usable record still needs Company ID, 40 descriptive characters and 8 descriptive words. Stable IDs remain yc:<Company ID>. One company remains one item; embedded fields remain One Liner, Tags, Long Description. Metadata remains company_name, company_id, industry, subindustry, batch, status and expanded yc_url. Descriptions are explicitly limited to the existing 256-token model input; 71 of the 1,000 required truncation. This includes the same five truncated documents in the first 50. Company names are not added as a separate embedding field.

Before insertion, the loader verifies that existing IDs belong to the selection and existing documents and metadata match the rebuilt selection. A saved pre-expansion snapshot was subsequently compared to actual database contents: all original 50 documents, metadata and embedding vectors are exactly unchanged, as are all 10 original smoke records. The collection was not deleted or recreated.

## Loading and actual persistence checks

| Metric | Expansion process | Loader rerun (new process) |
|---|---:|---:|

| Rows inspected | 1046 | 1046 |

| Selected | 1000 | 1000 |

| Count before | 50 | 1000 |

| Added | 950 | 0 |

| Count after | 1000 | 1000 |

| Unique IDs | 1000 | 1000 |

| Unique documents | 1000 | 1000 |

| Embedding/insertion seconds | 43.18141279090196 | 1.5830155462026596e-06 |

| Loading setup + insertion seconds | 43.70340166706592 | 0.6225374999921769 |

| Total seconds from loader entry through loading checks | 43.84072274994105 | 0.7500794171355665 |

| Smoke collection count | 10 | 10 |

Skipped: {'insufficient_description': 46}. No missing-ID or duplicate-ID skips occurred. The 950 additions were sent in nine batches of 100 and one batch of 50. Progress was printed after every batch, ending at 1,000 / 1,000. Download time and subsequent search time are excluded from loading timing.

Expansion process exited successfully before the loader rerun. A further fresh Python process opened the existing collection using get_collection() and asserted count == 1000; it did not create a collection. It also verified preserved vectors and records. Rerunning added zero records. No duplicate IDs or duplicate stored document texts were present.

Query D was chosen before the 1,000-company searches: earned pay access is substantially different from education, recipes and meetings. Earlier 50-company evidence already included an earned-pay business, so D is not a blind benchmark. Its observed ranking is reported without alteration.

## Queries A–D: complete top 10 and manual judgments

These are manual judgments of the returned company descriptions, not generated application explanations or a competitor label. Lower default squared L2 distance means closer in embedding space; conceptual relevance still requires reading the text. Distances below are unrounded.

### Query A — focus/productivity

A tool that notices when college students drift to social media during homework and rewards them for staying focused.

| Rank | Company | Distance | Judgment | Description / reason |
|---|---|---:|---|---|

| 1 | Litnerd | 1.0913758277893066 | somewhat related | Gamified reading and writing for children; no distraction monitoring. |

| 2 | Scout | 1.120255708694458 | mostly irrelevant | School records and administrative automation, not personal focus. |

| 3 | Speak | 1.1482117176055908 | somewhat related | Language tutoring, but no focus detection or reward mechanism. |

| 4 | Eduflow | 1.1648690700531006 | somewhat related | Engaging online learning activities, not distraction control. |

| 5 | Virtually | 1.1754611730575562 | somewhat related | Attendance tracking and reminders for online schools. |

| 6 | Lingt | 1.1960467100143433 | somewhat related | Classroom language assignments; education overlap only. |

| 7 | Glimpse K12 | 1.2163715362548828 | mostly irrelevant | School spending and outcome analytics. |

| 8 | Padlet | 1.224035620689392 | somewhat related | Engaging documents, not attention monitoring. |

| 9 | Platzi | 1.2319737672805786 | somewhat related | Online courses with high completion; no focus tool. |

| 10 | Matter | 1.23789381980896 | somewhat related | Reading app; no distraction detection or incentives. |

#### 1. Litnerd

Stored embedded document:

Summary: Reading + Writing Club App for Kids
Tags: education; saas; media; kids
Description: Litnerd is a kids reading + writing club app that grew by 14x this past school year. Think of us as a modern-day Scholastic, with a heavy IP play. We create original IP with our community + partner brands -> turn them into books, media and learning curriculum, layered with an AI personalized tutor to help kids learn to read and write in a personalized and engaging way.

Our product format is a Social and Gamified - with a live weekly community meetup and monthly e-tournaments. 

- And it works! Litnerd 4x improved the pass rate of students on their annual state Reading (ELA) exam.
- STICKY: Kids spend 10-20 minutes on the Litnerd app OUTSIDE of classroom time.
- KID AUTHORS: Kids are the authors of the books and Litnerd AI helps illustrate + publish the book.
- Built on the Science of Reading
- Original IP: all books, media and courseware is original content created and published by Litnerd.

Relevant metadata:

```json
{
  "company_name": "Litnerd",
  "status": "Active",
  "batch": "Summer 2021",
  "subindustry": "Education",
  "company_id": "24558",
  "yc_url": "https://www.ycombinator.com/companies/litnerd",
  "industry": "Education"
}
```

Distance: 1.0913758277893066

#### 2. Scout

Stored embedded document:

Summary: AI-powered student information system for K-12 schools
Tags: education; workflow-automation; ai
Description: The student information system (SIS) is the core system of record in every K-12 school. It tracks students, attendance, grades, schedules, staff, and more - kind of like the ERP for schools.

Legacy SIS providers do just about that, and not much more. School districts layer dozens of tools on top of their SIS to fill in the gaps.

Scout is an AI-powered student information system that automates school- and district-wide busywork, from day-to-day operations like attendance tracking to annual compliance reports. Our mission is to help school districts run like high-performing organizations, enabling them to provide high-quality, personalized instruction to every student.

Relevant metadata:

```json
{
  "industry": "Education",
  "company_name": "Scout",
  "batch": "Winter 2025",
  "subindustry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/scout-4",
  "company_id": "30205",
  "status": "Active"
}
```

Distance: 1.120255708694458

#### 3. Speak

Stored embedded document:

Summary: A superhuman, AI-powered language tutor in your pocket
Tags: artificial-intelligence; education

Relevant metadata:

```json
{
  "industry": "Consumer",
  "yc_url": "https://www.ycombinator.com/companies/speak",
  "status": "Active",
  "company_name": "Speak",
  "batch": "Winter 2017",
  "subindustry": "Consumer -> Social",
  "company_id": "1443"
}
```

Distance: 1.1482117176055908

#### 4. Eduflow

Stored embedded document:

Summary: Create and run collaborative online learning experiences.
Tags: education; elearning
Description: Eduflow is a tool for running active online learning experiences. We are used at thousands of institutions around the world all the way from middle school to corporate training at Google. We believe that digital tools for learning need to be more than just a playlist of videos. We're building learning activities that instructors can use to engage learners and make them active participants in their own learning process.

Relevant metadata:

```json
{
  "subindustry": "Education",
  "yc_url": "https://www.ycombinator.com/companies/eduflow",
  "industry": "Education",
  "batch": "Summer 2017",
  "status": "Acquired",
  "company_id": "1674",
  "company_name": "Eduflow"
}
```

Distance: 1.1648690700531006

#### 5. Virtually

Stored embedded document:

Summary: The "Shopify" for Online Schools
Tags: education; saas; elearning
Description: The first ever "Student Relationship Manager" for online schools to bridge the gap between educators and students. Track attendance on Zoom, send reminders, and more.

Relevant metadata:

```json
{
  "company_id": "22049",
  "company_name": "Virtually",
  "status": "Inactive",
  "industry": "B2B",
  "yc_url": "https://www.ycombinator.com/companies/virtually",
  "batch": "Summer 2020",
  "subindustry": "B2B"
}
```

Distance: 1.1754611730575562

#### 6. Lingt

Stored embedded document:

Summary: Lingt provided a web-based platform for learning languages leveraging…
Tags: education
Description: Lingt empowers teachers to speak more with their students. Create and manage online speaking assignments for use in the classroom.

Relevant metadata:

```json
{
  "company_name": "Lingt",
  "batch": "Summer 2009",
  "yc_url": "https://www.ycombinator.com/companies/lingt",
  "status": "Active",
  "company_id": "259",
  "subindustry": "Education",
  "industry": "Education"
}
```

Distance: 1.1960467100143433

#### 7. Glimpse K12

Stored embedded document:

Summary: Glimpse eliminates ineffective spending in schools.
Tags: education; analytics
Description: Glimpse12 captures everything you're doing to impact student outcomes and evaluates these activities in the context of student achievement.

Traditionally, eROI is virtually impossible to track and manage. The company's approach maximizes district's education return on investment (eROI) by providing answers to critical questions essential to ensure your time and money are aligned with the unique needs of your students.

Relevant metadata:

```json
{
  "batch": "Winter 2018",
  "subindustry": "Education",
  "company_id": "1774",
  "yc_url": "https://www.ycombinator.com/companies/glimpse-k12",
  "company_name": "Glimpse K12",
  "industry": "Education",
  "status": "Acquired"
}
```

Distance: 1.2163715362548828

#### 8. Padlet

Stored embedded document:

Summary: Papyrus → Parchment → Paper → Padlet
Tags: education; saas
Description: We are easily bored. It's the one thing that unites humanity in 2020. No one wants to read twenty paragraphs of text, or sit through forty verbose slides. Yet, we keep making them, boring everyone out of their minds.

We are building more beautiful and fun alternatives to traditional documents. They're less of a pain-in-the-ass to create, and a lot less waterboard-y to view.

Checkout a Padlet timeline (https://padl.et/timeline), or a Padlet map (https://padl.et/map) to see what we're talking about. 

Over ten million people all over the world use Padlet. Most satisfyingly, for millions of kids, Padlet is their first experience of creating things on the Internet.

People say we are improving education. People say we are making them more creative. People say a lot of things.

Relevant metadata:

```json
{
  "batch": "Winter 2013",
  "company_id": "481",
  "industry": "B2B",
  "yc_url": "https://www.ycombinator.com/companies/padlet",
  "status": "Active",
  "company_name": "Padlet",
  "subindustry": "B2B -> Productivity"
}
```

Distance: 1.224035620689392

#### 9. Platzi

Stored embedded document:

Summary: Latin America's School of Technology
Tags: education; elearning; video; hr-tech; subscriptions
Description: Platzi cracked online education. It teaches courses on design, marketing and programming with a 70% completion rate, to over one million students worldwide.

The classes include real-time collaboration among students and industry leaders as teachers. It aims to be the professional home for lifelong learning of advanced skills.

Relevant metadata:

```json
{
  "batch": "Winter 2015",
  "company_name": "Platzi",
  "yc_url": "https://www.ycombinator.com/companies/platzi",
  "subindustry": "Education",
  "industry": "Education",
  "company_id": "774",
  "status": "Active"
}
```

Distance: 1.2319737672805786

#### 10. Matter

Stored embedded document:

Summary: Building the future of reading
Description: Matter is a powerful, modern reading app that lets you save media from anywhere, pulls in your newsletters, lets you listen to your articles in a natural voice, and much more.

Relevant metadata:

```json
{
  "status": "Active",
  "industry": "Consumer",
  "batch": "Summer 2020",
  "yc_url": "https://www.ycombinator.com/companies/matter",
  "subindustry": "Consumer -> Content",
  "company_name": "Matter",
  "company_id": "22327"
}
```

Distance: 1.23789381980896

### Query B — food waste/recipes

People describe what's sitting in their fridge and get dinner suggestions before their groceries go bad.

| Rank | Company | Distance | Judgment | Description / reason |
|---|---|---:|---|---|

| 1 | Jupiter | 1.2333773374557495 | somewhat related | Food creators and groceries; no pantry-to-recipe evidence in stored text. |

| 2 | Unfurl | 1.284945011138916 | somewhat related | Family food delivery, not meals from existing ingredients. |

| 3 | Chowdeck | 1.2996286153793335 | somewhat related | Restaurant delivery; no recipe or waste workflow. |

| 4 | MilkRun | 1.3262288570404053 | somewhat related | Farm deliveries include recipe suggestions, but not existing-fridge input. |

| 5 | OneStopKitchen | 1.33585524559021 | somewhat related | Restaurant inventory and operations rather than household meal planning. |

| 6 | Bistrobot | 1.3418421745300293 | somewhat related | Sandwich-making robot, not suggestions from pantry contents. |

| 7 | Instacart | 1.3488410711288452 | somewhat related | Grocery fulfillment rather than cooking with food already owned. |

| 8 | Membo | 1.3608644008636475 | somewhat related | Fresh grocery delivery, not household food-waste recipes. |

| 9 | The Essential | 1.3703527450561523 | somewhat related | Essentials retail with food-tech tags; no pantry planning. |

| 10 | Prompt | 1.4139606952667236 | mostly irrelevant | Relationship management for professionals. |

#### 1. Jupiter

Stored embedded document:

Summary: Using AI to help food creators verticalize food
Tags: grocery; marketplace; e-commerce; food-&-beverage; advertising

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/jupiter",
  "subindustry": "Consumer -> Home and Personal",
  "batch": "Summer 2019",
  "company_id": "12574",
  "company_name": "Jupiter",
  "industry": "Consumer",
  "status": "Active"
}
```

Distance: 1.2333773374557495

#### 2. Unfurl

Stored embedded document:

Summary: A virtual food hall that delivers
Tags: delivery; food-tech
Description: Unfurl is a ghost kitchen, but instead of having one type of food we enable families to order many types of food all in one order. Think of it as an upscale food court where you and your kids can order from 8-15 different restaurants all at once.

Relevant metadata:

```json
{
  "industry": "Consumer",
  "subindustry": "Consumer -> Food and Beverage",
  "status": "Inactive",
  "company_name": "Unfurl",
  "company_id": "22675",
  "yc_url": "https://www.ycombinator.com/companies/unfurl",
  "batch": "Winter 2021"
}
```

Distance: 1.284945011138916

#### 3. Chowdeck

Stored embedded document:

Summary: On-demand food delivery for Africa
Tags: logistics
Description: Founded in October 2021, currently based in Lagos, Nigeria, Africa’s most populous city, Chowdeck is an on-demand food delivery service and marketplace where people can purchase their favourite meals from a wide range of restaurants. Whether local or continental, customers can buy food in a few short steps and have it delivered to their doorstep in under 30 minutes. 

Chowdeck is on a mission to empower restaurants in Africa to deliver meals to customers anywhere and anytime. Part of our unique offering to the restaurants listed on our marketplace is that we’ll help them grow, and so far, most of the restaurants we work with can boast of this achievement. With their help and the help of an ambitious team of relentless and fearless riders, we’ve delivered over 80,000 meals in the last six months in two major cities in Lagos.

We’ve come this far because we’re passionate about understanding the teething pains of delivery service in Africa and believe strongly in a world where ordering a meal is seamless.

Relevant metadata:

```json
{
  "company_name": "Chowdeck",
  "company_id": "26903",
  "subindustry": "Consumer -> Food and Beverage",
  "industry": "Consumer",
  "status": "Active",
  "batch": "Summer 2022",
  "yc_url": "https://www.ycombinator.com/companies/chowdeck"
}
```

Distance: 1.2996286153793335

#### 4. MilkRun

Stored embedded document:

Summary: Get Food From Farmers, Delivered.
Tags: e-commerce; supply-chain; agriculture
Description: Our team of farmers and chefs curate boxes of the finest quality local food for our customers each week. From seasonal produce, to humanely-handled pasture-raised meat, to organic eggs and dairy, there's something for every family. We deliver right to your door, as often as you want. Whether your family needs a delivery once a week or once a month, we're committed to helping you shop local. Delivery includes recipe suggestions, cooking videos, and more from our team of chefs. Whether you're looking for advice on how to roast a whole chicken or what that new-to-you vegetable is, we're here for you every step of the way.

Relevant metadata:

```json
{
  "company_name": "MilkRun",
  "status": "Inactive",
  "company_id": "22205",
  "industry": "Consumer",
  "yc_url": "https://www.ycombinator.com/companies/milkrun",
  "batch": "Summer 2020",
  "subindustry": "Consumer -> Food and Beverage"
}
```

Distance: 1.3262288570404053

#### 5. OneStopKitchen

Stored embedded document:

Summary: AI-Driven Tech & Space Optimization to Scale Restaurants
Tags: ghost-kitchens; e-commerce; ai
Description: OneStopKitchen (OSK) offers advanced technology and an innovative model which allows any restaurant to scale to multiple locations at zero cost. OSK offers an entire suite of AI powered advanced restaurant inventory, ops and logistics tech to scale quickly with limited risk. OSK operationalizes underperforming restaurant space and staff to run OSK kitchens which are located in prime downtowns and high walk-in areas. Think of AirBnB for restaurants. OSK is a preferred restaurant partner due to its innovative hyper scalable model. Consumers can mix & match multiple cuisines in a single order for dine in, pick up or delivery.

Relevant metadata:

```json
{
  "industry": "Consumer",
  "company_name": "OneStopKitchen",
  "status": "Active",
  "subindustry": "Consumer -> Food and Beverage",
  "batch": "Summer 2021",
  "yc_url": "https://www.ycombinator.com/companies/onestopkitchen",
  "company_id": "24302"
}
```

Distance: 1.33585524559021

#### 6. Bistrobot

Stored embedded document:

Summary: We make robots that make sandwiches.
Tags: food-service-robots-&-machines
Description: Bistrobot makes robots that make sandwiches. No more long lines and no more wrong orders, just good food fast. And the coolest part is you get to watch a robot make you lunch.

Relevant metadata:

```json
{
  "company_id": "906",
  "company_name": "Bistrobot",
  "subindustry": "B2B -> Retail",
  "batch": "Summer 2015",
  "yc_url": "https://www.ycombinator.com/companies/bistrobot",
  "status": "Inactive",
  "industry": "B2B"
}
```

Distance: 1.3418421745300293

#### 7. Instacart

Stored embedded document:

Summary: Marketplace for grocery delivery and pickup
Tags: grocery; delivery; e-commerce
Description: Instacart is the North American leader in online grocery and one of the fastest-growing companies in e-commerce. Instacart’s same-day delivery and pickup services bring fresh groceries and everyday essentials to busy people and families across the U.S. and Canada in as fast as an hour. Since its founding in 2012, Instacart has become an essential service for millions of families, while also serving as an immediate, flexible earnings opportunity for hundreds of thousands of shoppers across North America.  The company partners with more than 350 retailers and delivers from more than 25,000 stores across more than 5,500 cities in North America. Today, Instacart is accessible to more than 85% of households in the U.S. and more than 70% of households in Canada.

Relevant metadata:

```json
{
  "company_id": "468",
  "industry": "Consumer",
  "company_name": "Instacart",
  "status": "Public",
  "yc_url": "https://www.ycombinator.com/companies/instacart",
  "batch": "Summer 2012",
  "subindustry": "Consumer -> Food and Beverage"
}
```

Distance: 1.3488410711288452

#### 8. Membo

Stored embedded document:

Summary: Groceries fresher than a farmer’s market, delivered to you (EU)
Tags: grocery; marketplace; delivery
Description: Membo is a next-day grocery delivery app for premium customers in Europe. Like PinDuoDuo Groceries in China, Membo is the fastest way to order your weekly groceries directly from local food producers. The convenience of supermarkets & 15-minute grocery apps comes at the expense of freshness: food that should be delivered fresh, gets bought in bulk and sits on warehouse shelves for days. To get the freshest produce, you need quick producer-to-end-customer delivery, not just quick warehouse-to-customer delivery. Membo lets you order food directly from hundreds of local food producers & organises delivery so you always get the freshest version of every product. Membo's CEO, Vahur Hansen, was an early engineer at TransferWise, and co-founder, Paula Kink, built her own healthtech startup. Launched in Dec 2020, we've grown 30% MoM for the past 8 months and have delivered over 4000 orders in Tallinn, Estonia.

Relevant metadata:

```json
{
  "company_name": "Membo",
  "subindustry": "Consumer -> Food and Beverage",
  "company_id": "24692",
  "industry": "Consumer",
  "status": "Inactive",
  "batch": "Summer 2021",
  "yc_url": "https://www.ycombinator.com/companies/membo"
}
```

Distance: 1.3608644008636475

#### 9. The Essential

Stored embedded document:

Summary: E-commerce 2.0
Tags: e-commerce; food-tech
Description: The Essential is e-commerce 2.0.

What we do
We make and sell the single best version of all your essentials, at the best price possible.

How we do it
We're not an "everything store."We sell only the essentials, we're members-only and we only sell our own brand. We cut out the middlemen, the brands, the physical stores and the markups — to make products cost a lot less, all while paying the producer more.

Why we do it
To add meaning to people’s lives through
products they use and love, made by people who
know and care, with stories that matter, and
means that are honest.

Relevant metadata:

```json
{
  "industry": "Consumer",
  "subindustry": "Consumer",
  "company_name": "The Essential",
  "yc_url": "https://www.ycombinator.com/companies/the-essential",
  "batch": "Winter 2017",
  "company_id": "1475",
  "status": "Active"
}
```

Distance: 1.3703527450561523

#### 10. Prompt

Stored embedded document:

Summary: Helping busy professionals understand and maintain their relationships
Tags: crm

Relevant metadata:

```json
{
  "status": "Inactive",
  "batch": "Summer 2019",
  "industry": "B2B",
  "subindustry": "B2B -> Infrastructure",
  "company_id": "12570",
  "yc_url": "https://www.ycombinator.com/companies/prompt",
  "company_name": "Prompt"
}
```

Distance: 1.4139606952667236

### Query C — meeting follow-up

Software that listens to meetings and automatically turns conversations into organized follow-up tasks.

| Rank | Company | Distance | Judgment | Description / reason |
|---|---|---:|---|---|

| 1 | Onward | 0.7686163783073425 | genuinely conceptually similar | Explicitly automates post-meeting follow-ups, CRM updates and ticket creation. |

| 2 | Fathom | 0.8351094722747803 | somewhat related | Records/transcribes and clips important conversation moments; manual tagging, not explicit automatic task creation. |

| 3 | DailyBot | 0.9807789325714111 | somewhat related | Chat-based workflow automation and standups; no meeting listening described. |

| 4 | Moots AI | 0.9843339920043945 | somewhat related | Captures event leads/context and automates follow-up; different input workflow. |

| 5 | Findly | 1.0117197036743164 | mostly irrelevant | Chat-based business data analysis, not meeting-to-task conversion. |

| 6 | Cairns Health | 1.0316388607025146 | mostly irrelevant | Conversational chronic-care companion, not workplace meeting follow-up. |

| 7 | Argovox | 1.0403666496276855 | mostly irrelevant | Patient billing/collections voice agents, not meeting notes. |

| 8 | Warmly, | 1.0609254837036133 | somewhat related | Automated lead follow-up, but no meeting listening. |

| 9 | Aftercare | 1.0712798833847046 | mostly irrelevant | Survey follow-up questions rather than meeting action items. |

| 10 | Trace | 1.0979840755462646 | somewhat related | Routes tasks and automates workflows; no meeting capture described. |

#### 1. Onward

Stored embedded document:

Summary: Intelligent meeting automation for ambitious teams.
Description: Onward is a new take on conversational intelligence. We streamline follow-ups, CRM updates, ticket creation, and other tasks after every meeting—helping you connect this knowledge to the rest of your tools.

Relevant metadata:

```json
{
  "batch": "Summer 2023",
  "status": "Inactive",
  "yc_url": "https://www.ycombinator.com/companies/onward",
  "company_name": "Onward",
  "subindustry": "B2B -> Productivity",
  "company_id": "29124",
  "industry": "B2B"
}
```

Distance: 0.7686163783073425

#### 2. Fathom

Stored embedded document:

Summary: Never take notes again with the #1 AI Meeting Assistant
Tags: saas; b2b
Description: Instead of trying to hurriedly take notes while also having a conversation, you simply push a button in our app whenever you hear something important, like a piece of product feedback or action item. In real-time our system records, transcribes, and creates clips from the parts of the conversation you tagged that can share with your team or use to write post-call notes.

Relevant metadata:

```json
{
  "industry": "B2B",
  "batch": "Winter 2021",
  "yc_url": "https://www.ycombinator.com/companies/fathom",
  "subindustry": "B2B -> Productivity",
  "company_name": "Fathom",
  "company_id": "22879",
  "status": "Active"
}
```

Distance: 0.8351094722747803

#### 3. DailyBot

Stored embedded document:

Summary: AI Assistant and Chat Add-ons for Work
Tags: developer-tools; saas; collaboration; ai; ai-assistant
Description: DailyBot is a chat AI Assistant and Workflow Automation platform. It takes chat to a new level by providing automation and chat use-cases that are underserved by the current messaging platforms. It helps users get more things done within the chat to be more efficient and save time.

The new generation lives in chat. Remote/hybrid teams use DailyBot to automate daily workflows like stand-ups, team check-ins, give kudos to teammates or even to create their own chat-automation for their back-office with no-code/low-code in an environment similar to Amazon Alexa. DailyBot offers numerous add-ons to make the work experience better.

DailyBot provides a ChatGPT assistant and a unique AI Workflows tool. Users can build multi-step workflows that use AI to generate content, process information and run actions.

DailyBot is cross platform and already available for Slack, Microsoft Teams, Google Chat and Discord.

Keywords: chatops chat-ops async nocode assistant workflow automation developer

Relevant metadata:

```json
{
  "industry": "B2B",
  "subindustry": "B2B -> Productivity",
  "status": "Active",
  "yc_url": "https://www.ycombinator.com/companies/dailybot",
  "batch": "Summer 2021",
  "company_id": "24153",
  "company_name": "DailyBot"
}
```

Distance: 0.9807789325714111

#### 4. Moots AI

Stored embedded document:

Summary: Scan badges at business events, build context, and follow up with AI
Tags: collaboration; social-network; crm; ai; ai-assistant
Description: Going to trade shows or conferences? Moots AI helps you turn contacts into deals.

We’re building an AI tool that helps you capture leads, keep track of key details, and follow up fast  starting with in-person events.

Moots AI is a smart contact system for sales teams, founders, investors, recruiters, and partnership managers who rely on real-world events to meet leads, close deals, and build relationships. Our first focus: make sure no lead from a conference, summit, or meetup slips through the cracks.

Relevant metadata:

```json
{
  "batch": "Winter 2022",
  "company_name": "Moots AI",
  "company_id": "25279",
  "status": "Active",
  "industry": "Consumer",
  "subindustry": "B2B -> Productivity",
  "yc_url": "https://www.ycombinator.com/companies/moots-ai"
}
```

Distance: 0.9843339920043945

#### 5. Findly

Stored embedded document:

Summary: Co-pilot for Business Intelligence
Tags: artificial-intelligence; generative-ai; b2b; chatbot; data-engineering
Description: Findly.ai is the co-pilot for Business Intelligence that revolutionizes how businesses understand and interact with their data. By creating an engaging chat environment, it empowers decision-makers to gain insights, request reports, and generate visualizations based on their company's metrics. This seamless interaction is made possible by integrating a metric layer that comprehends all your company's metrics. The chat-based exploration simplifies complex data analysis, allowing users to generate comprehensive summaries with a single click, which can be exported to various formats. Furthermore, with the introduction of scheduled chats and action-triggered automations, Findly.ai enhances the autonomy and efficiency of decision-makers. It's more than a tool; it's a decision-making operational system aiming to facilitate decision-makers in achieving their KPIs while spending less time waiting for data.

Relevant metadata:

```json
{
  "subindustry": "B2B -> Analytics",
  "status": "Active",
  "industry": "B2B",
  "company_name": "Findly",
  "batch": "Summer 2022",
  "yc_url": "https://www.ycombinator.com/companies/findly",
  "company_id": "27097"
}
```

Distance: 1.0117197036743164

#### 6. Cairns Health

Stored embedded document:

Summary: Your voice. Your health. We care.
Tags: hardware; machine-learning; consumer-health-services
Description: Cairns Health is creating a fundamentally better healthcare experience for people with chronic health conditions and those who care for them. We make healthcare more accessible by simplifying complex care plans, connecting care teams and meeting patients where they live. Through our conversational AI, patients use their voice to interact with our digital care companion, who proactively gives medication reminders, symptom checks, behavioral nudges and even engages in friendly conversation to ease loneliness. Cairns uses a device that includes radar to put the patient in context and passively monitors their activities, including: heart rate, breathing rate and sleep stages, all without a wearable. The result is informed and timely intervention that drives improved clinical outcomes, reduced care delivery costs and a more satisfactory healthcare experience for all.

Relevant metadata:

```json
{
  "company_name": "Cairns Health",
  "company_id": "1638",
  "subindustry": "Healthcare -> Consumer Health and Wellness",
  "yc_url": "https://www.ycombinator.com/companies/cairns-health",
  "batch": "Summer 2017",
  "industry": "Healthcare",
  "status": "Active"
}
```

Distance: 1.0316388607025146

#### 7. Argovox

Stored embedded document:

Summary: Voice AI agents for patient billing and collections
Tags: fintech; healthcare; legaltech; call-center; ai-assistant
Description: We help healthcare providers increase profitability and cashflow by automating their patient billing and collections processes.

Today, healthcare providers in the US are leaving up to 20% of their profit margins on the table due to subpar patient billing and collections processes. Billing patients and collecting their payments is a complex process that requires specialized skills and a lot of effort. Traditionally, healthcare providers have done this manually, with limited automation around one-way reminders. This leads to limited engagement with payers and subpar collection results.

Argovox changes this by making new levels of payer engagement possible at scale. Through both voice and text conversations, our AI agents can engage in complex, multi-turn patient billing and collection conversation. This leads higher engagement with payers and optimal collection results.

Relevant metadata:

```json
{
  "industry": "Fintech",
  "subindustry": "Fintech",
  "yc_url": "https://www.ycombinator.com/companies/argovox",
  "status": "Inactive",
  "company_id": "27045",
  "company_name": "Argovox",
  "batch": "Summer 2022"
}
```

Distance: 1.0403666496276855

#### 8. Warmly,

Stored embedded document:

Summary: Autonomous sales platform to auto-email your warmest leads
Tags: b2b; productivity; sales; sales-enablement; ai
Description: Step 1: We find you warm leads: contacts + companies that are showing interest on your website (via 6sense/Clearbit) and researching you around the web (via Bombora) but haven't converted yet.

Step 2: We then auto follow up via chat, email or LinkedIn. Depends what workflows you want to set up - we can AI chat with them on your website, auto AI email them via your sequence provider of choice, and/or auto AI linkedin sequence them. Your humans can verify everything before being sent too. 

Outcome: 10x more outbound than a human SDR, 3x reply rates since they're warm and more booked meetings (results shown in ROI dashboard). 

P.S. if you want to use humans: you can send 1-click warm intro requests via your network or live chat/video call them too.

This is the power of an autonomous sales orchestration platform and we have 100+ paying customers who can back it up.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/warmly",
  "status": "Active",
  "batch": "Summer 2020",
  "subindustry": "B2B -> Sales",
  "company_name": "Warmly,",
  "industry": "B2B",
  "company_id": "22241"
}
```

Distance: 1.0609254837036133

#### 9. Aftercare

Stored embedded document:

Summary: Conversational AI surveys with intelligent follow-up questions
Tags: saas; productivity; feedback; data-visualization
Description: Aftercare helps you run surveys with AI-powered follow-up questions to dig into responses for deeper insights—it’s like having a skilled interviewer for every survey.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/aftercare",
  "batch": "Winter 2024",
  "industry": "B2B",
  "status": "Active",
  "company_id": "29383",
  "subindustry": "B2B -> Operations",
  "company_name": "Aftercare"
}
```

Distance: 1.0712798833847046

#### 10. Trace

Stored embedded document:

Summary: Workflow automation that routes tasks to humans and AI
Tags: artificial-intelligence; saas; b2b; workflow-automation; productivity
Description: Trace is a workflow automation platform that routes tasks to the right agent – human or AI. We enable enterprise-grade context and AI orchestration in mid-sized teams. 

Trace breaks workflows into clear steps, sends repetitive tasks to AI agents, and routes the rest to the right people while respecting permissions and logging every action. 

We help teams cut busywork and unify AI tools across departments – helping companies adopt AI in days rather than months.

Relevant metadata:

```json
{
  "batch": "Summer 2025",
  "subindustry": "Fintech",
  "status": "Active",
  "industry": "B2B",
  "company_id": "30687",
  "company_name": "Trace",
  "yc_url": "https://www.ycombinator.com/companies/trace-so"
}
```

Distance: 1.0979840755462646

### Query D — earned pay access

A service that lets employees withdraw money they have already earned instead of waiting until the end of the month.

| Rank | Company | Distance | Judgment | Description / reason |
|---|---|---:|---|---|

| 1 | Forfeit | 1.158424735069275 | mostly irrelevant | Habit enforcement via monetary penalties, not earned-pay access. |

| 2 | Milio | 1.178505301475525 | somewhat related | Immediate payment rails; not earned wages specifically. |

| 3 | Tranch | 1.1871185302734375 | somewhat related | Accelerates enterprise invoice payments; different customer and workflow. |

| 4 | Payflow | 1.2134134769439697 | genuinely conceptually similar | Employees can access salary whenever they want instead of monthly or biweekly. |

| 5 | Wibond | 1.25392746925354 | somewhat related | Consumer purchase credit rather than early access to wages. |

| 6 | PayCaddy | 1.2598512172698975 | somewhat related | Wallet/payment infrastructure can serve employees; no earned-pay promise. |

| 7 | SlidePay | 1.2763659954071045 | mostly irrelevant | In-person card acceptance API, not employee wage access. |

| 8 | Pide Directo | 1.2948342561721802 | mostly irrelevant | Restaurant management and payment tools. |

| 9 | Dayra | 1.297564148902893 | genuinely conceptually similar | Offers unbanked workers early advances on earnings, including truck drivers; loans rather than necessarily earned-wage withdrawal. |

| 10 | CashBook | 1.3038604259490967 | somewhat related | Employee expense wallets rather than access to earned compensation. |

#### 1. Forfeit

Stored embedded document:

Summary: An app that takes your money if you don't complete your habits.
Tags: mental-health-tech; consumer; fitness; productivity; digital-health
Description: Say what you're going to do, when you're going to do it, and how much money you'll forfeit if you don't do it. Send photo or timelapse evidence of you completing the habit by the time you set, or we take your money.

Eg, I could set it to go to the gym (or meditate for 30 mins, or take a photo of a sent email, or of a max amount of calories on MyFitnessPal) tomorrow at 6am, or lose $30. If I don't send photo evidence in the gym (that we manually approve), I lose $30.

Relevant metadata:

```json
{
  "batch": "Winter 2023",
  "company_id": "27898",
  "industry": "Consumer",
  "subindustry": "Consumer -> Home and Personal",
  "status": "Active",
  "yc_url": "https://www.ycombinator.com/companies/forfeit",
  "company_name": "Forfeit"
}
```

Distance: 1.158424735069275

#### 2. Milio

Stored embedded document:

Summary: B2B-2C real-time account to account payments
Tags: fintech; saas; payments; b2b
Description: Milio is a fully interoperable and immediate payment system for Colombia through a single API connected to millions of accounts. Milio allows companies to perform payable and receivable in real time without ACH rails.

We provide our solution through two Plug and Play integrations:

PID payment button:
End-to-end, white label, native, non-redirection payment technology for your customers to pay you account-to-account more efficiently than PSE, without heavy and inefficient ACH cycles and fixed rates.

Technology: API, SDK, Checkout UI.

Immediate disbursement:
Single API connection to all banks, allowing any company or person to disburse 24/7, in real-time, with immediate crediting of funds to third parties at any bank or digital wallet.

Technology: API, Dashboard UI.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/milio",
  "company_name": "Milio",
  "subindustry": "Fintech",
  "company_id": "28007",
  "status": "Active",
  "batch": "Winter 2023",
  "industry": "Fintech"
}
```

Distance: 1.178505301475525

#### 3. Tranch

Stored embedded document:

Summary: Tranch is the invoice to payments platform for enterprises.
Tags: fintech; saas
Description: Tranch is the invoice to payments platform for enterprises who want to optimize cash flow by offering their business clients an unparalleled payment experience.

Based out of New York City and London we enable Services firms, software and marketplaces to be paid faster via our automated invoice to payment solutions. Our frictionless payment methods include Pay Now via FedNow, Pay by Card, Pay by Crypto and Pay Later from 2 to 12 months up to $1M.

Find out more about how we simplify and accelerate accounts receivables for enterprises with the most innovative workflows and payment solutions at www.tranch.com.

Tranch is backed by leading investors including: Global Founders Capital, TracVC, UpHonest Capital, Soma Capital, FoundersX and Y Combinator.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/tranch",
  "industry": "Fintech",
  "company_name": "Tranch",
  "batch": "Summer 2022",
  "subindustry": "Fintech -> Payments",
  "company_id": "26764",
  "status": "Acquired"
}
```

Distance: 1.1871185302734375

#### 4. Payflow

Stored embedded document:

Summary: A mobile app. It allows employees to get paid their salary on-demand.
Tags: fintech; saas; hr-tech; lending
Description: A mobile app. It allows employees to get paid whenever they want, instead of just once a month (or biweekly). We sell it to companies as an employee benefit (B2B SaaS).

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/payflow",
  "batch": "Summer 2021",
  "company_name": "Payflow",
  "industry": "B2B",
  "company_id": "24874",
  "status": "Active",
  "subindustry": "B2B -> Human Resources"
}
```

Distance: 1.2134134769439697

#### 5. Wibond

Stored embedded document:

Summary: Affirm for LATAM
Tags: banking-as-a-service; cashierless-checkout; fintech
Description: Under "Buy Now, Pay Later" business model, Wibond is a 100% flexible digital payment method enabling the 200 million underbanked consumers without credit cards to shop online for the first time. 

We integrate directly into the purchase flow of online merchants, and we offer consumers a credit, when they have already made up their mind that they want to acquire a specific product.
We provide financial and digital access to a large community of people offering payment options according to their possibilities and profile. Wibond is an inclusive and simple solution:
 - Consumers can create their free account to quickly access and pay without banks, in installments, and without a card.
 - Merchants with e-commerce channels increase their sales and integrate Wibond in a very agile way by offering a new form of payment and expanding their markets.

We’re also integrated in the purchase flow of more than 500 merchants, including Samsung, Musimundo (one of the Biggest retailers in LATAM) , and Motorola. And up to 65% of the payment transactions on these sites go through us.

Relevant metadata:

```json
{
  "subindustry": "Fintech -> Credit and Lending",
  "status": "Active",
  "industry": "Fintech",
  "company_id": "25665",
  "batch": "Winter 2022",
  "company_name": "Wibond",
  "yc_url": "https://www.ycombinator.com/companies/wibond"
}
```

Distance: 1.25392746925354

#### 6. PayCaddy

Stored embedded document:

Summary: Simplified Banking as a Service for Latam
Tags: banking-as-a-service; fintech; b2b
Description: PayCaddy enables Latam companies to launch financial products with an API based platform. Rather than building fintech from scratch, or dealing with a legacy bank, companies can use PayCaddy to open digital wallets with KYC checks, automate online payments, and issue personalized debit and prepaid cards for customers or employees.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/paycaddy",
  "company_name": "PayCaddy",
  "industry": "Fintech",
  "status": "Active",
  "batch": "Winter 2022",
  "company_id": "25660",
  "subindustry": "Fintech"
}
```

Distance: 1.2598512172698975

#### 7. SlidePay

Stored embedded document:

Summary: Banking and Payment Platform APIs. Exited October 2014.
Tags: fintech; payments; api
Description: SlidePay, formerly Cube, is an API that makes it easy for any app to accept credit cards that are processed in person. Integration takes hours, not weeks, and works on any platform or device.

Relevant metadata:

```json
{
  "batch": "Winter 2012",
  "company_name": "SlidePay",
  "subindustry": "Fintech -> Payments",
  "company_id": "20",
  "yc_url": "https://www.ycombinator.com/companies/slidepay",
  "industry": "Fintech",
  "status": "Acquired"
}
```

Distance: 1.2763659954071045

#### 8. Pide Directo

Stored embedded document:

Summary: One-stop-shop for restaurants to operate and grow their business.
Tags: autonomous-delivery; saas; e-commerce; enterprise-software
Description: Pidedirecto is a restaurant management platform that optimizes operations, increases revenue, and enhances customer experience. Its comprehensive toolset includes point of sale, payment terminals, online ordering, delivery management, loyalty programs, and integrations with third-party services.

All for a reasonable fixed monthly fee, without eating up margins with hefty commissions and service charges.

Relevant metadata:

```json
{
  "subindustry": "B2B -> Supply Chain and Logistics",
  "yc_url": "https://www.ycombinator.com/companies/pide-directo",
  "company_id": "24882",
  "industry": "B2B",
  "status": "Active",
  "batch": "Summer 2021",
  "company_name": "Pide Directo"
}
```

Distance: 1.2948342561721802

#### 9. Dayra

Stored embedded document:

Summary: Data-driven embedded Financial Services for Gig Workers
Tags: banking-as-a-service; fintech
Description: Dayra makes it easy for Egyptian businesses offer Loans and virtual bank accounts to their unbanked workers and customers through their App.
For example, one of our customers an Egyptian trucking marketplace uses our API to give truck drivers an early advance on their earnings.

Relevant metadata:

```json
{
  "industry": "Fintech",
  "batch": "Winter 2021",
  "yc_url": "https://www.ycombinator.com/companies/dayra",
  "company_name": "Dayra",
  "company_id": "23405",
  "subindustry": "Fintech -> Credit and Lending",
  "status": "Active"
}
```

Distance: 1.297564148902893

#### 10. CashBook

Stored embedded document:

Summary: Ramp for Indian Businesses - UPI Wallets for Employee Expenses
Tags: fintech; saas; b2b
Description: Issue UPI wallets to employees, track and control the spend.

Relevant metadata:

```json
{
  "batch": "Winter 2021",
  "company_name": "CashBook",
  "industry": "B2B",
  "yc_url": "https://www.ycombinator.com/companies/cashbook",
  "status": "Active",
  "company_id": "22745",
  "subindustry": "B2B -> Finance and Accounting"
}
```

Distance: 1.3038604259490967

### Nonsense

Quantum marshmallow nebula dances inside a purple theorem.

| Rank | Company | Distance | Judgment | Description / reason |
|---|---|---:|---|---|

| 1 | Zenflow | 1.7256138324737549 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 2 | Turion Space | 1.7364881038665771 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 3 | SlidePay | 1.7375915050506592 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 4 | Hubble Network | 1.7415380477905273 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 5 | Clew | 1.766330361366272 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 6 | Butter | 1.7750520706176758 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 7 | Apolink | 1.7750816345214844 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 8 | Wifi Dabba, Inc. | 1.791759729385376 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 9 | Streem | 1.7923266887664795 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

| 10 | Zenedy | 1.7935348749160767 | mostly irrelevant | No meaningful product concept in the nonsense query; nearest available vector only. |

#### 1. Zenflow

Stored embedded document:

Summary: Medical device that provides a more effective, less invasive…
Tags: medical-devices
Description: Forty million men in the US and over 500 million worldwide suffer from urinary obstruction related to benign prostatic hyperplasia (BPH). The majority of men will experience symptoms of this disease at some point in life. BPH, also known as prostate enlargement, leads to urinary straining, frequency, urgency, and sleep disruption. Despite the high prevalence and significant quality of life burden of BPH, established treatments are limited to drugs, which have limited effectiveness, and surgery, which carries a high risk of sexual side effects. The Zenflow Spring is a small implant delivered in the urologist's office in a simple procedure that provides quick and long-lasting symptom relief.

Relevant metadata:

```json
{
  "batch": "Winter 2015",
  "status": "Active",
  "industry": "Healthcare",
  "yc_url": "https://www.ycombinator.com/companies/zenflow",
  "subindustry": "Healthcare -> Medical Devices",
  "company_id": "834",
  "company_name": "Zenflow"
}
```

Distance: 1.7256138324737549

#### 2. Turion Space

Stored embedded document:

Summary: Moving Things Around in Space, Imaging Space Objects When We're Not
Tags: space-exploration; satellites
Description: Turion Space is building spacecraft to move things around in space and image space objects when they’re not, and focused on developing the dual-use technology required to ensure a sustainable future in space. They aim to build a strong foundation selling space domain awareness imagery data while advancing their technology towards an affordable solution for orbital debris removal and eventually asteroid mining. The founding team originates from SpaceX, and after going through the Y-combinator accelerator in summer 2021 went on to raise a $6.2M seed round and is launching their first DROID satellite in early 2023.

Relevant metadata:

```json
{
  "company_id": "24865",
  "status": "Active",
  "subindustry": "Industrials -> Aviation and Space",
  "industry": "Industrials",
  "company_name": "Turion Space",
  "yc_url": "https://www.ycombinator.com/companies/turion-space",
  "batch": "Summer 2021"
}
```

Distance: 1.7364881038665771

#### 3. SlidePay

Stored embedded document:

Summary: Banking and Payment Platform APIs. Exited October 2014.
Tags: fintech; payments; api
Description: SlidePay, formerly Cube, is an API that makes it easy for any app to accept credit cards that are processed in person. Integration takes hours, not weeks, and works on any platform or device.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/slidepay",
  "industry": "Fintech",
  "company_name": "SlidePay",
  "subindustry": "Fintech -> Payments",
  "company_id": "20",
  "status": "Acquired",
  "batch": "Winter 2012"
}
```

Distance: 1.7375915050506592

#### 4. Hubble Network

Stored embedded document:

Summary: Bluetooth to Space
Tags: developer-tools; hard-tech; hardware; iot; satellites
Description: Hubble is building a global satellite network that any Bluetooth-enabled device can connect to, even without cellular reception.  Our mission in life is to get a billion devices connected to the network and unlock a new era of human-machine collaboration.

Relevant metadata:

```json
{
  "industry": "Industrials",
  "status": "Active",
  "yc_url": "https://www.ycombinator.com/companies/hubble-network",
  "company_name": "Hubble Network",
  "subindustry": "Industrials -> Aviation and Space",
  "company_id": "25313",
  "batch": "Winter 2022"
}
```

Distance: 1.7415380477905273

#### 5. Clew

Stored embedded document:

Summary: Unified file system for the cloud.
Tags: saas; b2b
Description: Clew lets employees see and organize files across their work apps from one place.

Relevant metadata:

```json
{
  "subindustry": "B2B -> Infrastructure",
  "company_id": "21997",
  "company_name": "Clew",
  "industry": "B2B",
  "status": "Acquired",
  "yc_url": "https://www.ycombinator.com/companies/clew",
  "batch": "Summer 2020"
}
```

Distance: 1.766330361366272

#### 6. Butter

Stored embedded document:

Summary: Behavioral Cache for Agents
Tags: developer-tools; generative-ai; cloud-computing
Description: Butter is building Muscle Mem, an SDK for recording and deterministically replaying tool call trajectories. Our goal is to get LLMs out of the hotpath for repetitive tasks, increasing speed, reducing variability, and eliminating token costs for the many cases that could have just been a script.

Relevant metadata:

```json
{
  "industry": "B2B",
  "status": "Active",
  "batch": "Winter 2025",
  "subindustry": "B2B -> Infrastructure",
  "company_name": "Butter",
  "company_id": "30335",
  "yc_url": "https://www.ycombinator.com/companies/butter"
}
```

Distance: 1.7750520706176758

#### 7. Apolink

Stored embedded document:

Summary: 24/7 satellite connectivity in low Earth orbit
Description: Apolink is building the world’s most interoperable satellite relay network in low Earth orbit. Our hybrid communication architecture combines RF and optical inter-satellite links to enable real-time, continuous connectivity for satellite operators across industries.

Relevant metadata:

```json
{
  "status": "Active",
  "company_id": "30130",
  "batch": "Fall 2024",
  "yc_url": "https://www.ycombinator.com/companies/apolink",
  "subindustry": "Industrials -> Aviation and Space",
  "company_name": "Apolink",
  "industry": "Industrials"
}
```

Distance: 1.7750816345214844

#### 8. Wifi Dabba, Inc.

Stored embedded document:

Summary: Decentralised broadband connectivity.
Tags: hardware; crypto-web3; telecommunications
Description: We enable humans & machines with internet connectivity at a price that they can afford.

The inspiration for Wifi Dabba came from the founders working together for the last decade in the mobile application industry and realising the biggest reason for user churn being access to cheap and affordable internet access. From having worked on ground onboarding users and facing poor connectivity issues all the time, we took it on ourselves to fix the internet access problem for the common citizen.

At Wifi Dabba (YC W17), we are building a low cost, scalable & distributed Wi-Fi infrastructure to connect next billion users online. We do this by deploying a grid of lasers (Free Space Optics) over the cities & town and bring cheap and fast internet for everyone. We enable anyone to buy 1 gig of data access at a time at a price they can afford. Sachetization of internet access is the foundation to rebuilding internet for all. We do this by leveraging crypto and blockchain to truly make internet infrastructure ownership distributed — our vision is to be connectivity layer for the Web3 world.

Relevant metadata:

```json
{
  "batch": "Winter 2017",
  "company_name": "Wifi Dabba, Inc.",
  "subindustry": "Consumer -> Home and Personal",
  "yc_url": "https://www.ycombinator.com/companies/wifi-dabba-inc",
  "status": "Active",
  "company_id": "1535",
  "industry": "Consumer"
}
```

Distance: 1.791759729385376

#### 9. Streem

Stored embedded document:

Summary: Acquired by Box in June 2014. We built: (1) a native win/mac…
Description: Streem (https://www.streem.com) offers unlimited cloud storage for your media. Store, stream, and share all your favorite movies, photos, music, and more with your friends!

Streem is a magical drive on your device that lives in the cloud and gives you unlimited space. You can put files into Streem, free up space on your computer and mobile devices, and instantly access and share your content anywhere, anytime. Unlike other cloud storage tools, Streem takes up no space on your computer, but still gives you instant access to your files without any lag. All media on Streem is converted on-the-fly so you can access it seamlessly regardless of the device or bandwidth.

Relevant metadata:

```json
{
  "yc_url": "https://www.ycombinator.com/companies/streem",
  "industry": "Consumer",
  "company_id": "401",
  "subindustry": "Consumer -> Content",
  "batch": "Summer 2012",
  "status": "Acquired",
  "company_name": "Streem"
}
```

Distance: 1.7923266887664795

#### 10. Zenedy

Stored embedded document:

Description: Zenedy
Zenedy was started as a means to showcase information about obscure topics from around the web.

Relevant metadata:

```json
{
  "batch": "Winter 2010",
  "subindustry": "Consumer -> Content",
  "company_id": "227",
  "industry": "Consumer",
  "status": "Inactive",
  "company_name": "Zenedy",
  "yc_url": "https://www.ycombinator.com/companies/zenedy"
}
```

Distance: 1.7935348749160767

## Four alternative realistic queries, tested

A–D did not establish two convincing low-keyword-overlap examples. After reading the actual corpus and results, four alternative queries were stated and tested once each. These are corpus-informed exploratory candidates, not held-out evaluation or invented user prompts. The failed wages candidate is retained. No target documents were edited or added.

### Scattered work documents

A single place to find documents scattered across all the online services my team uses.

Clew at #2 is a genuinely similar aggregation concept. User Hero at #1 is narrower user-research organization, only somewhat related. Clew is a useful additional semantic example.

| Rank | Company | Distance |
|---|---|---:|

| 1 | User Hero | 1.1168444156646729 |

| 2 | Clew | 1.1465065479278564 |

| 3 | GoLinks | 1.1540071964263916 |

| 4 | AeroFS | 1.1861575841903687 |

| 5 | Clarm | 1.1922050714492798 |

| 6 | Key Values | 1.21079421043396 |

| 7 | Algolia | 1.2122548818588257 |

| 8 | Iambiq Technologies | 1.243401288986206 |

| 9 | Herald | 1.2596275806427002 |

| 10 | WriteWith | 1.2681992053985596 |

#### 1. User Hero

Summary: A hub for all your user research.
Tags: saas; b2b; design-tools
Description: User Hero collects all your user research in one place. Organize studies, transcribe interviews, take notes collaboratively, tag and search observations, and more. We automatically generate reports and rainbow charts so your team can learn and build faster.

```json
{
  "batch": "Summer 2018",
  "company_name": "User Hero",
  "subindustry": "B2B -> Engineering, Product and Design",
  "company_id": "1890",
  "yc_url": "https://www.ycombinator.com/companies/user-hero",
  "status": "Inactive",
  "industry": "B2B"
}
```

#### 2. Clew

Summary: Unified file system for the cloud.
Tags: saas; b2b
Description: Clew lets employees see and organize files across their work apps from one place.

```json
{
  "company_name": "Clew",
  "industry": "B2B",
  "status": "Acquired",
  "company_id": "21997",
  "subindustry": "B2B -> Infrastructure",
  "yc_url": "https://www.ycombinator.com/companies/clew",
  "batch": "Summer 2020"
}
```

#### 3. GoLinks

Summary: Intuitive, easy-to-remember short links - powered by AI.
Tags: saas; productivity; collaboration
Description: GoLinks allows you to create internal links for your company that are so easy to remember and share, you don't have to bookmark or copy and paste them in emails. For example, teams use GoLinks to keep track of their dashboard at go/metrics or an employee directory at go/directory - powered by AI. These internal link systems have been a standard for productivity boost within companies like Google, Yahoo, Linkedin, Twitter, and Airbnb for years. GoLinks is the first company building this as a service for everyone else. 75% of all employees at all of our customers use GoLinks every single month.



In 2023, GoLinks, launched two new productivity solutions to build off of their vision of building a Gen AI productivity suite:


- GoSearch (www.gosearch.ai):  An enterprise workplace search solution powered by AI.


- GoProfiles (www.goprofiles.io): A hub for your team to find shared connections, celebrate wins, and boost company culture — powered by gen AI!

```json
{
  "company_id": "11984",
  "industry": "B2B",
  "company_name": "GoLinks",
  "yc_url": "https://www.ycombinator.com/companies/golinks",
  "batch": "Winter 2019",
  "status": "Active",
  "subindustry": "B2B -> Productivity"
}
```

#### 4. AeroFS

Summary: Secure Enterprise Collaboration.
Tags: collaboration; security; enterprise
Description: AeroFS enterprise file sync and share & collaboration solution deploys on your infrastructure. Your files remain secured by your own security protocols, removing the risk associated with relying on your vendors to secure your data.

The service has a Dropbox like user experience.  Now, both the end user and the IT team can both get what they are looking for out of a file sharing tool.

We are funded by some of Silicon Valley's best investors and entrepreneurs:

Avalon Ventures
A16Z Seed
YCombinator
SVAngel
Chris Sacca (Lowercase Capital)
Maynard Webb (COO eBay)
Jerry Yang (Founder Yahoo!)
Paul Buchheit (Founder FriendFeed)

We're hiring!  https://aerofs.com/company/careers
You will have the opportunity to work as part of a small team. This means that you will be "CEO" of whatever you create. Our size gives us agility in ways that large companies do not have: We push out code almost daily (on a desktop platform!) to thousands of users.

We're not just building a company; we're building a family. Many of us are new to the area,

```json
{
  "subindustry": "B2B -> Infrastructure",
  "company_id": "183",
  "industry": "B2B",
  "company_name": "AeroFS",
  "status": "Acquired",
  "yc_url": "https://www.ycombinator.com/companies/aerofs",
  "batch": "Summer 2010"
}
```

#### 5. Clarm

Summary: Perplexity for internal docs
Description: Clarm is your AI-native search and agent builder on internal docs. We are the #1 alignment meeting killer.

Our first customers are delighted to pay us 10x less than they would spend on a Chief of Staff, creating daily product release notes, customer feedback analysis, capturing sales objections, and running dedicated customer support channels. The COO's hair is on fire and we put it out.

Our platform is built on agentic search, connecting across 40+ enterprise integrations - CRMs, email, knowledge bases.

Agents often fail because their underlying context windows are mismatched, leading them to hallucinate. We built enterprise native agentic search to ensure agents have all the context they need to operate fully autonomously.

Here's what Clarm's C-suite buyers use us for:

- a blockchain company to provide an on-demand source of product truth in natural language, reducing alignment meetings by 90%
- a financial services firm to supercharge their own product by integrating it with the target's enterprise knowledge
- the top 5 X25 open source startups (by star count) to increase engagement with their Github repo and knowledge base, turning

```json
{
  "yc_url": "https://www.ycombinator.com/companies/clarm",
  "batch": "Spring 2025",
  "status": "Active",
  "subindustry": "B2B -> Finance and Accounting",
  "company_id": "30439",
  "company_name": "Clarm",
  "industry": "B2B"
}
```

#### 6. Key Values

Summary: Helping software developers find teams that share their values.
Tags: recruiting; careers

```json
{
  "batch": "Winter 2018",
  "company_id": "1750",
  "company_name": "Key Values",
  "status": "Active",
  "industry": "B2B",
  "subindustry": "B2B -> Recruiting and Talent",
  "yc_url": "https://www.ycombinator.com/companies/key-values"
}
```

#### 7. Algolia

Summary: A developer-friendly and enterprise-grade search API.
Tags: developer-tools; saas; b2b
Description: Our mission is to make every search interaction meaningful & rewarding, through developer-friendly and enterprise-grade APIs.

Algolia is the leading Search & Discovery API for websites and mobile apps. We help the most innovative companies across e-commerce, media and SaaS industries create powerful, relevant and scalable discovery experiences for their users. Unlike other solutions, our hosted platform reduces the complexities of building and scaling a fast, relevant digital experience and helps teams accelerate development time. More than 9,000 companies like Under Armour, Twitch, Periscope, Medium and Stripe rely on Algolia to manage 50+ billion search queries a month.

Founded in 2012, we're backed by $184M in funding from Accel Partners, Alven Capital, Point Nine Capital and Storm Ventures. The team is headquartered in San Francisco with offices in Paris, London, New York, and Atlanta. To learn more, visit www.algolia.com.

---
We’re looking for talented, passionate people to build the world’s best search technology. As an ownership-driven company, we seek team

```json
{
  "status": "Active",
  "company_id": "636",
  "yc_url": "https://www.ycombinator.com/companies/algolia",
  "batch": "Winter 2014",
  "subindustry": "B2B -> Engineering, Product and Design",
  "industry": "B2B",
  "company_name": "Algolia"
}
```

#### 8. Iambiq Technologies

Description: We help organizations read and process large amounts of text-based data usually handled by humans.

```json
{
  "company_id": "1853",
  "batch": "Winter 2018",
  "industry": "B2B",
  "subindustry": "B2B -> Engineering, Product and Design",
  "status": "Inactive",
  "company_name": "Iambiq Technologies",
  "yc_url": "https://www.ycombinator.com/companies/iambiq-technologies"
}
```

#### 9. Herald

Summary: A collaborative repository for user feedback.
Tags: customer-success; team-collaboration
Description: Herald helps product and customer teams work together to grow  revenue by painting a full picture of user problems.

We start by providing the best experience for capturing customer feedback from the most relevant apps: Intercom, Front, Email, Slack, and more. Then, Herald's robust analytical engine helps you rigorously qualify and quantify customer feedback according to your business goals.

Herald molds to the way your team works: it can be used exclusively as an internal tool, in semi-private mode to share a history of their feedback with specific customers, or publicly by publishing a  product roadmap and changelog.

```json
{
  "subindustry": "B2B -> Office Management",
  "industry": "B2B",
  "status": "Inactive",
  "company_name": "Herald",
  "company_id": "11982",
  "yc_url": "https://www.ycombinator.com/companies/herald",
  "batch": "Winter 2019"
}
```

#### 10. WriteWith

Description: Writewith is a collaborative writing web app, enabling you to easily flow through the steps of writing, editing, and publishing a document with a group. A document is started by uploading an existing document (.doc, .txt, .rdf) or just typing away. After the initial draft is completed, you can invite other editors by email and assign them tasks. Writewith has full version control and even lets you post comments to each other, making it possible to edit together in real time. Currently Writewith is in beta testing with 15 college newspapers including Stanford and two of Canada's largest college papers (which even includes a national newswire).

```json
{
  "subindustry": "Consumer -> Content",
  "industry": "Consumer",
  "company_name": "WriteWith",
  "yc_url": "https://www.ycombinator.com/companies/writewith",
  "batch": "Winter 2007",
  "company_id": "350",
  "status": "Inactive"
}
```

### Flexible wages

Let staff collect part of their compensation whenever they need it, rather than waiting for a scheduled payroll date.

Failed as a positive example: none of the returned top 10 establishes flexible access to already-earned wages. Medical scheduling/billing and general payroll tools dominate. Payflow was not in the top 10 for this paraphrase.

| Rank | Company | Distance |
|---|---|---:|

| 1 | Cero | 1.3020546436309814 |

| 2 | Argovox | 1.3096771240234375 |

| 3 | Bemlo | 1.333048701286316 |

| 4 | Claim Health | 1.3468669652938843 |

| 5 | FirstWork | 1.3843519687652588 |

| 6 | Central | 1.3912827968597412 |

| 7 | Plane | 1.3990345001220703 |

| 8 | Mendel | 1.411668062210083 |

| 9 | Hellobill | 1.4228699207305908 |

| 10 | Sira | 1.4295114278793335 |

#### 1. Cero

Summary: Automated communication between hospitals and patients in Latam
Tags: machine-learning; consumer-health-services; b2b; nlp
Description: At Cero, we solve specific coordination tasks between hospitals and patients, such as appointment confirmations and last minute cancellations, by automatically communicating with patients over WhatsApp. For example, a patient can confirm and reschedule their appointment without needing to call anyone.

Almost half of the medical appointments in Latin America are missed because patients simply do not show up. This ranges from missing a regular dentist check to missing an expensive MRI scan. With increasing pressure to improve access to care in developing countries, optimizing communication and coordination with patients is a key task to achieve. This is a massive problem especially in places where most people don't know how to effectively use self-service mediums (or are too busy to use them).
 
We bootstrapped the company and we are profitable. As of August 2021 we have $97K in monthly revenue from 15 clients with a CMRG of 20% in the last year. We have 100% logo retention and we grow with our clients. We are currently coordinating over 600,000 medical appointments every month, just in Chile.

This problem represents a $3

```json
{
  "batch": "Summer 2021",
  "company_name": "Cero",
  "subindustry": "B2B",
  "status": "Active",
  "industry": "B2B",
  "company_id": "24303",
  "yc_url": "https://www.ycombinator.com/companies/cero"
}
```

#### 2. Argovox

Summary: Voice AI agents for patient billing and collections
Tags: fintech; healthcare; legaltech; call-center; ai-assistant
Description: We help healthcare providers increase profitability and cashflow by automating their patient billing and collections processes.

Today, healthcare providers in the US are leaving up to 20% of their profit margins on the table due to subpar patient billing and collections processes. Billing patients and collecting their payments is a complex process that requires specialized skills and a lot of effort. Traditionally, healthcare providers have done this manually, with limited automation around one-way reminders. This leads to limited engagement with payers and subpar collection results.

Argovox changes this by making new levels of payer engagement possible at scale. Through both voice and text conversations, our AI agents can engage in complex, multi-turn patient billing and collection conversation. This leads higher engagement with payers and optimal collection results.

```json
{
  "subindustry": "Fintech",
  "status": "Inactive",
  "industry": "Fintech",
  "batch": "Summer 2022",
  "yc_url": "https://www.ycombinator.com/companies/argovox",
  "company_id": "27045",
  "company_name": "Argovox"
}
```

#### 3. Bemlo

Summary: AI-native scheduling and workforce management platform for healthcare
Tags: artificial-intelligence; saas; b2b; healthcare; enterprise-software
Description: Bemlo is an AI-driven workforce management platform, specifically tailored for the healthcare and social care sectors, with automated scheduling as its cornerstone. The system generates optimal schedules that balance care demands with employee preferences, freeing up valuable time for patient care, enhancing workplace satisfaction, and promoting more efficient collaboration within organizations.

```json
{
  "subindustry": "Healthcare -> Healthcare IT",
  "batch": "Winter 2022",
  "company_name": "Bemlo",
  "yc_url": "https://www.ycombinator.com/companies/bemlo",
  "company_id": "25825",
  "industry": "Healthcare",
  "status": "Active"
}
```

#### 4. Claim Health

Summary: The first AI revenue platform for post-acute healthcare
Description: Post-acute agencies lose up to 15% of revenue each year to denials, non-compliant documentation, and delayed payments. Most treat it as a cost of doing business. Instead of waiting weeks for rejections and appealing claims one by one, Claim Health flags issues in real-time and automates claim corrections and appeals—before revenue is lost.

While working with healthcare providers, we found most denials stem from small, preventable documentation errors. As payor requirements grow increasingly complex and fragmented, billing has become a manual, error-prone process. Claim Health closes the loop between documentation and billing outcomes—using AI to detect issues, automate workflows, and recover thousands in missed revenue each week.

Kevin and JJ bring nearly a decade of experience building and scaling healthtech companies. At Dandy, JJ was a founding engineer and Kevin was the first GTM hire; together they helped grow the business from 0 to $150M+ ARR. At Perry (now Jolly), JJ led engineering and Kevin was Head of Sales, driving the company through a $16.5M Series A led by Tesla’s former CFO.

In under three weeks since incorporation, we

```json
{
  "company_id": "30429",
  "industry": "Healthcare",
  "status": "Active",
  "subindustry": "Healthcare",
  "company_name": "Claim Health",
  "batch": "Spring 2025",
  "yc_url": "https://www.ycombinator.com/companies/claim-health"
}
```

#### 5. FirstWork

Summary: Rippling for seasonal workers
Tags: artificial-intelligence; saas; human-resources; workflow-automation; compliance
Description: Firstwork is a next-generation HR platform designed specifically for companies with dynamic workforce needs. Our mission is to streamline and automate key HR processes to help businesses operate more efficiently and effectively.

What We Do (for now):

(1) Smart Onboarding 📋: Our platform simplifies the onboarding process by automating the collection and verification of credentials, such as right-to-work documents, insurance forms and driver’s licenses. This reduces administrative burden and accelerates the time-to-productivity for new hires.

(2) AI-Assisted Activation 🤖: Leveraging AI, we enhance communication and messaging for new hires, ensuring they receive timely and relevant information. This helps in better engagement and faster integration into their roles.

(3) Perpetual Compliance ✅: Our system uses AI and OCR technology to continuously monitor and ensure compliance with various regulatory requirements. This includes tracking expirations of critical documents, updating records, and generating compliance reports, thus reducing the risk of penalties and legal issues.

```json
{
  "company_name": "FirstWork",
  "batch": "Summer 2024",
  "status": "Active",
  "company_id": "29651",
  "subindustry": "B2B -> Human Resources",
  "industry": "B2B",
  "yc_url": "https://www.ycombinator.com/companies/firstwork"
}
```

#### 6. Central

Summary: Payroll, benefits, state compliance & other bullsh*t for startups
Tags: artificial-intelligence; fintech; b2b; hr-tech; payroll
Description: Central kills back-office work for startups. While HR/payroll platforms give you software to figure it out, Central actually does all the work using AI agents and human experts: payroll, benefits, compliance, accounting, taxes, and more. That's 10+ hours back every month. 

Thousands of founders trust Central, including high-growth companies like Magic Patterns, Wordware, and Bitesight.

Learn more and start for free at centralhq.com

```json
{
  "yc_url": "https://www.ycombinator.com/companies/central",
  "industry": "B2B",
  "status": "Active",
  "company_name": "Central",
  "subindustry": "B2B -> Human Resources",
  "company_id": "29327",
  "batch": "Summer 2024"
}
```

#### 7. Plane

Summary: #1 easiest-to-use payroll for startups
Tags: fintech; saas; b2b; compliance; hr-tech
Description: Plane is an all-in-one people platform for fast-growing teams. We build easy-to-use payroll and compliance tools that help companies go global from day one.

```json
{
  "company_id": "1517",
  "yc_url": "https://www.ycombinator.com/companies/plane",
  "company_name": "Plane",
  "subindustry": "B2B -> Human Resources",
  "industry": "B2B",
  "batch": "Winter 2017",
  "status": "Active"
}
```

#### 8. Mendel

Summary: Workflows to empower employees to spend while finance stay in control
Tags: fintech; b2b

```json
{
  "batch": "Winter 2021",
  "industry": "Fintech",
  "company_name": "Mendel",
  "status": "Active",
  "company_id": "23240",
  "yc_url": "https://www.ycombinator.com/companies/mendel",
  "subindustry": "Fintech -> Banking and Exchange"
}
```

#### 9. Hellobill

Summary: Hellobill aggregates all your business bills, automatically, every…
Tags: fintech; payments
Description: Imagine if all your PDF bills could be automatically downloaded every month for your accountant ? 

Say hi to Hellobill.
 
Hellobill is a 1-click solution that automatically downloads all your online PDF bills for your accountant. Uber, Amazon, AWS, Google Apps, Adwords, Facebook Ads, but also utilities bills and many more. 
 
Our users

Hellobill is specifically designed for CEOs, CFOs, Managers and Office Managers that are tired of manual & tedious low-value accounting tasks. 

Our mission

To put an end to the monthly nightmare associated with accounting in SMB. Thanks to Hellobill, our users refocus on what’s important: their business.

Hellobill’s added value

- Improve your efficiency
Do more work in less time with an intuitive software
- Increase productivity
With data flowing automatically, you will make your work easier and faster.
- Focus on adding value
Automate basic functions, freeing up your time for the things that matters.

How does it work?

1. Download the Hellobill desktop app
2. Log in to all your online providers’ accounts once & for all
3. Click on “Fetch my bills” and that'

```json
{
  "company_id": "1203",
  "company_name": "Hellobill",
  "subindustry": "B2B -> Finance and Accounting",
  "batch": "Summer 2016",
  "yc_url": "https://www.ycombinator.com/companies/hellobill",
  "status": "Inactive",
  "industry": "B2B"
}
```

#### 10. Sira

Summary: AI Native Rippling for Deskless Workers
Tags: artificial-intelligence; b2b; hr-tech
Description: Sira is the AI-powered platform for managing time tracking, scheduling, payroll, and HR — purpose-built for hourly teams.

Our intelligent agents handle the manual, time-consuming tasks for you — like calling workers to fill open shifts, detecting timesheet anomalies, and streamlining payroll processing.

With Sira, businesses stay organized, compliant, and focused on what really matters — while we take care of the team.

```json
{
  "company_name": "Sira",
  "company_id": "30742",
  "industry": "B2B",
  "status": "Active",
  "yc_url": "https://www.ycombinator.com/companies/sira",
  "subindustry": "B2B -> Human Resources",
  "batch": "Summer 2025"
}
```

### Livestock health

A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.

Cowlar at #1 is genuinely similar: neck-worn cattle monitoring that identifies illness and helps reproduction. The next result, meat delivery, is mostly irrelevant. Some human health wearables overlap technically but are not livestock products.

| Rank | Company | Distance |
|---|---|---:|

| 1 | Cowlar | 0.96701580286026 |

| 2 | Sendme, Inc | 1.2627296447753906 |

| 3 | Vena Vitals | 1.3076263666152954 |

| 4 | Lifted | 1.320949912071228 |

| 5 | Zeit Medical | 1.338008165359497 |

| 6 | iLabService | 1.3430553674697876 |

| 7 | Dr. Treat | 1.3627197742462158 |

| 8 | Cairns Health | 1.3670705556869507 |

| 9 | Avion | 1.368905782699585 |

| 10 | Equipt Health | 1.3694534301757812 |

#### 1. Cowlar

Summary: Fitbit for dairy cows. Farms use cowlar's alerts & recommendations to…
Tags: machine-learning; iot; agriculture
Description: Cowlar, a fitbit for dairy cows provides data as a service to help dairy producers optimize operations and improve herd health.

It's simple. You strap it around a cow's neck. It measures temperature, activity and cow behavior. Cowlar makes sense of the data and sends the farmers actionable recommendations on how to:

1. Boost reproduction rates
2. Identify diseases instantly
3. Improve milk yield 
4. We can even tell if someone is stealing your cow ! 

Cowlar is simple, affordable and easy to use. It's rugged, water proof, comes with a 6 Month battery life so farmers dont have to worry about charging and farmers can be sent text messages in any language/ for those who cant read, we can send an automated phone call.

```json
{
  "yc_url": "https://www.ycombinator.com/companies/cowlar",
  "industry": "Industrials",
  "batch": "Winter 2017",
  "company_name": "Cowlar",
  "subindustry": "Industrials -> Agriculture",
  "status": "Inactive",
  "company_id": "1445"
}
```

#### 2. Sendme, Inc

Summary: On demand provider of meat to households and food businesses
Tags: artificial-intelligence; e-commerce; food-tech
Description: Sendme is an on-demand provider of clean meat to individuals and food businesses. We built a chatbot that lets customers place orders for meat on WhatsApp and they get it within 3hours.

```json
{
  "subindustry": "Consumer -> Food and Beverage",
  "status": "Active",
  "company_id": "25727",
  "industry": "Consumer",
  "company_name": "Sendme, Inc",
  "yc_url": "https://www.ycombinator.com/companies/sendme-inc",
  "batch": "Winter 2022"
}
```

#### 3. Vena Vitals

Summary: A small sticker that monitors blood pressure continuously
Tags: hard-tech; nanosensors; health-tech; medical-devices; digital-health
Description: Vena Vitals makes a small sticker that monitors blood pressure continuously. We've shown that it works in the operating room and is as accurate as the best tools doctors have today, at a fraction of the cost. We're a team of health tech scientists with multiple past startups and exits, and we've built products that have scaled to over 2M users.

```json
{
  "yc_url": "https://www.ycombinator.com/companies/vena-vitals",
  "status": "Active",
  "batch": "Summer 2020",
  "industry": "Healthcare",
  "subindustry": "Healthcare -> Medical Devices",
  "company_name": "Vena Vitals",
  "company_id": "22206"
}
```

#### 4. Lifted

Summary: Smartwatch powered coaching to improve teams sustainable performance
Tags: mental-health-tech; biometrics
Description: NudgeLabs is a service that helps enterprises improve team performance and employee retention. We pair each employee with an online coach and use smart watch data to improve their physical and mental health.

```json
{
  "company_name": "Lifted",
  "subindustry": "B2B -> Human Resources",
  "batch": "Winter 2022",
  "yc_url": "https://www.ycombinator.com/companies/lifted",
  "industry": "B2B",
  "status": "Active",
  "company_id": "25357"
}
```

#### 5. Zeit Medical

Summary: Immediate stroke detection at home
Tags: sleep-tech; consumer-health-services; medical-devices
Description: Zeit Medical leverages the power of AI and wearable sensors to deliver peace of mind for those affected by stroke. Zeit’s smart headband immediately detects the onset of stroke and notifies 911. Each year more than 90% of the one million strokes in the US go untreated, resulting in life-long disability and exploding medical costs north of $100b. The lack of timely treatment is the result of delays in alerting the emergency services. More than 10 million Americans with an elevated stroke risk live with constant fear that a stroke may go unnoticed for hours, while they are asleep or alone. The company was founded by Orestis Vardoulis  PhD  a biomedical & mechanical engineer and expert in digital health (EPFL/Stanford) and Urs Naber  MD  a critical care physician (Dartmouth/Stanford). They have both seen the devastating effects of stroke in their families and came up with the idea of addressing this unmet clinical need during their Stanford Biodesign Innovation Fellowship.

```json
{
  "subindustry": "Healthcare -> Medical Devices",
  "status": "Active",
  "industry": "Healthcare",
  "company_id": "24058",
  "yc_url": "https://www.ycombinator.com/companies/zeit-medical",
  "company_name": "Zeit Medical",
  "batch": "Summer 2021"
}
```

#### 6. iLabService

Summary: AI powered Lab Operation Management SaaS Platform
Tags: saas; iot; productivity
Description: We provide SaaS solution to boost your operational efficiency, enhance your safety management. One stop oversight of your lab operation and resource management, such as " Man, Machine, Material, Method and Health and Safety".

```json
{
  "status": "Active",
  "company_id": "2026",
  "subindustry": "B2B -> Productivity",
  "company_name": "iLabService",
  "batch": "Summer 2018",
  "yc_url": "https://www.ycombinator.com/companies/ilabservice",
  "industry": "B2B"
}
```

#### 7. Dr. Treat

Summary: “One Medical for pets.”
Tags: telehealth; consumer; digital-health
Description: Dr. Treat is a tech enabled modern veterinary care company offering virtual and in-clinic services to pet parents. We are building the largest pet health company powered by technology and driven by data to offer highly personalized & preventative care for every pet.

```json
{
  "batch": "Summer 2022",
  "industry": "Healthcare",
  "status": "Active",
  "subindustry": "Healthcare -> Healthcare Services",
  "yc_url": "https://www.ycombinator.com/companies/dr-treat",
  "company_id": "26735",
  "company_name": "Dr. Treat"
}
```

#### 8. Cairns Health

Summary: Your voice. Your health. We care.
Tags: hardware; machine-learning; consumer-health-services
Description: Cairns Health is creating a fundamentally better healthcare experience for people with chronic health conditions and those who care for them. We make healthcare more accessible by simplifying complex care plans, connecting care teams and meeting patients where they live. Through our conversational AI, patients use their voice to interact with our digital care companion, who proactively gives medication reminders, symptom checks, behavioral nudges and even engages in friendly conversation to ease loneliness. Cairns uses a device that includes radar to put the patient in context and passively monitors their activities, including: heart rate, breathing rate and sleep stages, all without a wearable. The result is informed and timely intervention that drives improved clinical outcomes, reduced care delivery costs and a more satisfactory healthcare experience for all.

```json
{
  "batch": "Summer 2017",
  "subindustry": "Healthcare -> Consumer Health and Wellness",
  "company_id": "1638",
  "status": "Active",
  "industry": "Healthcare",
  "yc_url": "https://www.ycombinator.com/companies/cairns-health",
  "company_name": "Cairns Health"
}
```

#### 9. Avion

Summary: Avion builds and operates autonomous eVTOL drones that deliver vital…
Tags: autonomous-delivery; drones
Description: Avion is a drone-based digital health platform, designed to bridge the gap between remote clinics and urban healthcare infrastructures. By connecting these isolated clinics with sophisticated labs and well-stocked pharmacies in cities, Avion brings a new era of remote diagnostics and prescription fulfilment.

Avion ensures the rapid, safe, and efficient delivery of vital medical supplies and clinical samples, even to the most hard-to-reach locations. 

Avion's operation uniquely combines cutting-edge autonomous drone technology with digital health platforms. Our drones, built with advanced eVTOL capabilities, ensure seamless take-off and landing capabilities, even in challenging terrains.

Avion's digital health platform serves as the connective tissue between urban health centers and remote clinics. The platform features an intuitive interface, making it easy for healthcare providers to order necessary supplies, track shipments, and even communicate with laboratory and pharmacy staff.

```json
{
  "batch": "Winter 2020",
  "yc_url": "https://www.ycombinator.com/companies/avion",
  "subindustry": "Industrials -> Drones",
  "company_id": "13477",
  "company_name": "Avion",
  "industry": "Industrials",
  "status": "Active"
}
```

#### 10. Equipt Health

Summary: Home medical equipment, prescribed online and delivered.
Tags: sleep-tech; consumer-health-services; digital-health; telemedicine
Description: Equipt Health makes it easy for any healthcare company to offer prescription medical devices to patients. We handle the whole process: the packaging, the logistics, the clinical (via our provider network) and technical support, and the return of data from connected devices. We're starting with the diagnosis and treatment of sleep apnea at heliosleep.com.

```json
{
  "status": "Active",
  "company_id": "24875",
  "subindustry": "Healthcare",
  "company_name": "Equipt Health",
  "batch": "Summer 2021",
  "yc_url": "https://www.ycombinator.com/companies/equipt-health",
  "industry": "Healthcare"
}
```

### Remote connectivity

Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.

Hubble Network at #2 is genuinely similar: connecting Bluetooth devices through satellites without cellular reception. Doblet at #1 addresses phone battery charging and is mostly irrelevant to connectivity. Apolink at #3 has satellite communication overlap, but serves satellite operators rather than everyday small gadgets.

| Rank | Company | Distance |
|---|---|---:|

| 1 | Doblet | 1.0344176292419434 |

| 2 | Hubble Network | 1.05861496925354 |

| 3 | Apolink | 1.0969836711883545 |

| 4 | Toymail | 1.1929928064346313 |

| 5 | Wifi Dabba, Inc. | 1.2560151815414429 |

| 6 | Radical | 1.2602519989013672 |

| 7 | Spire Health | 1.2792001962661743 |

| 8 | Circular | 1.2796131372451782 |

| 9 | Automatic | 1.2861487865447998 |

| 10 | Tsumobi | 1.29947829246521 |

#### 1. Doblet

Summary: Doblet solves the phone battery problem.  We're building the first…
Tags: hardware
Description: Doblet is the world’s first network of batteries on demand for charging phones everywhere. The company’s mission is to provide portable power anywhere consumers happen to be. Using patent-pending technology and the Doblet mobile app on iOS or Android devices, users are instantly notified of the nearest place to pick up a charge the moment their batteries start to run low. Consumers can charge their smartphones while on the go at over 1,000 San Francisco Bay Area cafes, bars, and restaurants.

```json
{
  "batch": "Summer 2014",
  "yc_url": "https://www.ycombinator.com/companies/doblet",
  "subindustry": "B2B -> Office Management",
  "status": "Inactive",
  "industry": "B2B",
  "company_name": "Doblet",
  "company_id": "667"
}
```

#### 2. Hubble Network

Summary: Bluetooth to Space
Tags: developer-tools; hard-tech; hardware; iot; satellites
Description: Hubble is building a global satellite network that any Bluetooth-enabled device can connect to, even without cellular reception.  Our mission in life is to get a billion devices connected to the network and unlock a new era of human-machine collaboration.

```json
{
  "company_name": "Hubble Network",
  "subindustry": "Industrials -> Aviation and Space",
  "batch": "Winter 2022",
  "industry": "Industrials",
  "yc_url": "https://www.ycombinator.com/companies/hubble-network",
  "status": "Active",
  "company_id": "25313"
}
```

#### 3. Apolink

Summary: 24/7 satellite connectivity in low Earth orbit
Description: Apolink is building the world’s most interoperable satellite relay network in low Earth orbit. Our hybrid communication architecture combines RF and optical inter-satellite links to enable real-time, continuous connectivity for satellite operators across industries.

```json
{
  "subindustry": "Industrials -> Aviation and Space",
  "company_name": "Apolink",
  "yc_url": "https://www.ycombinator.com/companies/apolink",
  "industry": "Industrials",
  "company_id": "30130",
  "status": "Active",
  "batch": "Fall 2024"
}
```

#### 4. Toymail

Summary: Connected toys that enable two-way voice messaging between children…
Tags: iot; kids
Description: The only kid-friendly WIFI toy messenger. Use our free app to message our toys from your phone & your child can reply right back!

After securing funding from both Amazon and Verizon and getting into Y Combinator, Toymail has just launched the "Talkies"​  - a quirky new line of plush toys that let friends and family exchange messages with kids for two-way voice talk. 

With Toymail's Talkies kids can: 

• Send messages to grownup's phones with the free Toymail app
• Send messages directly to other friend's Talkies.
• Play for hours on or offline with our on-board voice filtering software

```json
{
  "company_name": "Toymail",
  "subindustry": "Consumer -> Consumer Electronics",
  "company_id": "1001",
  "yc_url": "https://www.ycombinator.com/companies/toymail",
  "industry": "Consumer",
  "status": "Inactive",
  "batch": "Winter 2016"
}
```

#### 5. Wifi Dabba, Inc.

Summary: Decentralised broadband connectivity.
Tags: hardware; crypto-web3; telecommunications
Description: We enable humans & machines with internet connectivity at a price that they can afford.

The inspiration for Wifi Dabba came from the founders working together for the last decade in the mobile application industry and realising the biggest reason for user churn being access to cheap and affordable internet access. From having worked on ground onboarding users and facing poor connectivity issues all the time, we took it on ourselves to fix the internet access problem for the common citizen.

At Wifi Dabba (YC W17), we are building a low cost, scalable & distributed Wi-Fi infrastructure to connect next billion users online. We do this by deploying a grid of lasers (Free Space Optics) over the cities & town and bring cheap and fast internet for everyone. We enable anyone to buy 1 gig of data access at a time at a price they can afford. Sachetization of internet access is the foundation to rebuilding internet for all. We do this by leveraging crypto and blockchain to truly make internet infrastructure ownership distributed — our vision is to be connectivity layer for the Web3 world.

```json
{
  "subindustry": "Consumer -> Home and Personal",
  "company_name": "Wifi Dabba, Inc.",
  "batch": "Winter 2017",
  "company_id": "1535",
  "yc_url": "https://www.ycombinator.com/companies/wifi-dabba-inc",
  "industry": "Consumer",
  "status": "Active"
}
```

#### 6. Radical

Summary: Building persistent, high-performance infrastructure in the sky
Tags: drones; satellites; aerospace
Description: Radical’s StratoSats are autonomous platforms that provide satellite-like services on demand. They fly within Earth’s atmosphere to provide persistent, high performance infrastructure across applications in earth observation, connectivity, and more. Unlike satellites, StratoSats navigate freely without the need for rocket launches or orbits - reducing costs, increasing flexibility, and ensuring customers get the targeted coverage they need.

```json
{
  "yc_url": "https://www.ycombinator.com/companies/radical",
  "company_id": "27960",
  "status": "Active",
  "company_name": "Radical",
  "subindustry": "Industrials -> Aviation and Space",
  "batch": "Winter 2023",
  "industry": "Industrials"
}
```

#### 7. Spire Health

Summary: Remote patient monitoring for lung disease patients.
Tags: telehealth; medical-devices; digital-health
Description: We are a B2B medical device and data company passionate about providing remote monitoring solutions for the proactive care of chronic disease patients.
Our core expertise and IP is in continuous respiratory sensing. Spire Remote Patient Monitoring is used by pulmonologists and patients throughout the United States. To date our sensors have been worn by more than 150,000 people.

```json
{
  "company_name": "Spire Health",
  "batch": "Winter 2015",
  "industry": "Healthcare",
  "yc_url": "https://www.ycombinator.com/companies/spire-health",
  "subindustry": "Healthcare -> Consumer Health and Wellness",
  "status": "Acquired",
  "company_id": "853"
}
```

#### 8. Circular

Summary: Subscription consumer electronics for Asia
Tags: fintech; marketplace; consumer; e-commerce
Description: Circular is accelerating the adoption of the circular economy by making subscriptions the best way to access and experience tech: from smartphones, laptops, and headphones to gaming, VR and wearables.

Our customers get their hands on the best tech through low-cost, convenient subscriptions. They can pay monthly, keep it as long as they want, and if they love it, buy it. If they return it, we carefully refurbish it and pass it on to the next loving owner - radically extending its useful life.

```json
{
  "company_name": "Circular",
  "status": "Active",
  "company_id": "26054",
  "subindustry": "Consumer -> Consumer Electronics",
  "yc_url": "https://www.ycombinator.com/companies/circular",
  "industry": "Consumer",
  "batch": "Winter 2022"
}
```

#### 9. Automatic

Summary: Automatic connects your car to the rest of your digital life.
Tags: iot; automotive
Description: Our Mission: To empower drivers with knowledge about themselves and their cars so they can be safer and drive smarter. We believe you shouldn’t have to buy a new car to have a better driving experience, and that the phone in your pocket can bring the future of driving to today’s automobiles.

Who We Are: Automatic is based in San Francisco, but our team comes from every corner of the world. We obsess about creating beautiful and well-engineered products that make a real difference in people’s lives. We’re big on ideas, low on ego, and love working together.

```json
{
  "company_name": "Automatic",
  "status": "Acquired",
  "industry": "Consumer",
  "subindustry": "Consumer -> Consumer Electronics",
  "batch": "Summer 2011",
  "yc_url": "https://www.ycombinator.com/companies/automatic",
  "company_id": "130"
}
```

#### 10. Tsumobi

Summary: Messaging.
Tags: messaging
Description: Mobile applications have so far been nightmares to implement. It's often hard to gain adoption due to complicated installs and near impossible to get users to upgrade their version once the product has shipped. Tsumobi hopes to solve this problem by creating their own language. The new language will sit on top of J2ME and process applications downloaded (via URL) for Tsumobi enabled sites. This means that developers will be able to change Tsumobi applications on the fly and have Tsumobi enabled phones automatically get the updates just by visiting a link.

```json
{
  "company_name": "Tsumobi",
  "industry": "Consumer",
  "company_id": "345",
  "batch": "Winter 2007",
  "yc_url": "https://www.ycombinator.com/companies/tsumobi",
  "subindustry": "Consumer -> Social",
  "status": "Inactive"
}
```

## Best two observed semantic candidates

### 1. Cowlar — rank 1, distance 0.96701580286026

Query: A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.

The document describes a Fitbit for dairy cows strapped around the neck, measurements of temperature/activity/behavior, identifying diseases, and boosting reproduction rates. Important expressions differ: cattle versus dairy cows; ranchers versus farmers; ill versus diseases; ready to breed versus reproduction rates; device worn versus Fitbit strapped around the neck. The same monitoring and animal-health product concept is expressed through different vocabulary.

### 2. Hubble Network — rank 2, distance 1.05861496925354

Query: Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.

The document describes a global satellite network connecting Bluetooth-enabled devices without cellular reception. Important expressions differ: wireless gadgets versus Bluetooth-enabled devices; phones have no signal versus without cellular reception; equipment orbiting Earth versus satellite network / space. Doblet incorrectly outranked it, so this is evidence of a high-ranking meaningful match, not perfect ranking.

Clew is a third observed candidate: rank 2 at 1.1465065479278564 for "A single place to find documents scattered across all the online services my team uses." It describes a unified cloud file system where employees organize files across work apps. Documents versus files, online services versus work apps, and team versus employees differ; generic words such as place and across overlap.

These examples show meaningful matches despite differing important phrases. No keyword-search baseline was run, so they do not prove superiority over every keyword search system. They were discovered using this corpus, not independently validated. They are candidates for later assignment documentation, not a final README.

## Distance observations and coverage

| Query | Top-10 minimum | Top-10 maximum |
|---|---:|---:|

| Query A — focus/productivity | 1.0913758277893066 | 1.23789381980896 |

| Query B — food waste/recipes | 1.2333773374557495 | 1.4139606952667236 |

| Query C — meeting follow-up | 0.7686163783073425 | 1.0979840755462646 |

| Query D — earned pay access | 1.158424735069275 | 1.3038604259490967 |

| Nonsense | 1.7256138324737549 | 1.7935348749160767 |

| Scattered work documents | 1.1168444156646729 | 1.2681992053985596 |

| Flexible wages | 1.3020546436309814 | 1.4295114278793335 |

| Livestock health | 0.96701580286026 | 1.3694534301757812 |

| Remote connectivity | 1.0344176292419434 | 1.29947829246521 |

Genuinely similar examples include Onward (0.7686163783073425), Cowlar (0.96701580286026), Hubble Network (1.05861496925354), Clew (1.1465065479278564), Payflow (1.2134134769439697), and Dayra (1.297564148902893, with a lending-model caveat). Moderately related examples include Fathom (0.8351094722747803, manual tagging), Litnerd (1.0913758277893066, gamified learning), and MilkRun (1.3262288570404053, delivery with recipe suggestions).

Irrelevant or mismatched results can have comparatively small distances: Doblet battery charging (1.0344176292419434) outranks Hubble connectivity; Forfeit habit penalties (1.158424735069275) outranks Payflow earned-pay access. Findly business intelligence (1.0117197036743164) is closer numerically to the meeting query than some genuinely similar products are to other queries. Categories overlap substantially across queries.

Nonsense top-10 distances range from 1.7256138324737549 to 1.7935348749160767. In the earlier 50-company experiment, nonsense top-5 distances ranged from 1.8978135585784912 to 1.968353033065796. A larger pool supplies closer nearest neighbors even for nonsense; no universal threshold follows. These are distributions of retrieved top neighbors, not all 1,000 pairwise query-to-document distances.

One thousand companies appears sufficient for a bounded educational prototype with selected positive semantic examples, but not a reliable claim about idea originality or comprehensive competitor coverage. A and B still lack a genuinely close product in the returned top 10; their rank-1 results should not be called competitors. The failed wages paraphrase shows query sensitivity. Sector vocabulary, promotional text, short summaries and 71 truncated documents can distort ranking. Top-10 absence alone cannot establish absence from all 1,000 companies.

No clear technical failure requires a core data-model change at this stage. Keep one company per item and the existing descriptive text. Any later change to text selection or embeddings should be evaluated as a separate experiment rather than silently modifying this evidence.

## Errors and reproducibility

Expansion, rerun, fresh-process assertions and all nine queries completed without execution errors. The preexisting default embedding model cache was available. Dependencies, app.py, original smoke notes and 50-company report were not changed. The original prompt was appended verbatim to prompt_log.md. Raw snapshots and JSON results remain under ignored data/.

Run python3 load_yc.py to repeat the fixed 1,000-company selection and A–D/nonsense searches; existing records are skipped. This is an experiment loader, not a final CLI. This report preserves first expansion timing separately from the zero-insert rerun. The exact four alternative queries and their complete returned documents/metadata are preserved above and in ignored data/1000_alternatives.json.
