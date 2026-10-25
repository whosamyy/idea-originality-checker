# Reusable retrieval analysis verification

## Changed files and entry point

Added analysis.py, verify_analysis.py and this report. Appended the exact attached user prompt to prompt_log.md. app.py, load_yc.py, requirements.txt and all corpus records were left unchanged in this stage.

Call `from analysis import analyze_idea`, then `report = analyze_idea(description)`. No import-time queries or UI. analyze_idea validates nonempty text, opens the existing persistent yc_startups collection, retains mixed raw retrieval, separately queries the real YC IDs, cleans results, computes summaries, and returns a JSON-serializable dictionary. clean_matches and summarize_matches expose the intermediate steps as plain functions. No hosted APIs or LLMs are used.

## Exact return structure

```json
{
  "query": "str",
  "collection": "str",
  "collection_count": "int",
  "yc_record_count": "int",
  "raw_retrieval": {
    "all_items": "complete Chroma QueryResult",
    "real_companies": "complete YC-restricted Chroma QueryResult"
  },
  "all_matches": "list[Match], overall top 10",
  "user_created_matches": "list[Match], user subset of overall top 10; not all users in database",
  "real_company_matches": "list[Match], YC-restricted top 10",
  "closest_existing_companies": "list[Match], first 5 YC matches",
  "closest_known_analog": "Match or None, first YC match",
  "market_neighborhood": {
    "sample_size": "int",
    "industries": "list[{name: str, count: int}]",
    "subindustries": "list[{name: str, count: int}]",
    "distinct_industries": "int",
    "distinct_subindustries": "int",
    "missing_industry_count": "int",
    "missing_subindustry_count": "int",
    "distribution": "unknown | single_recorded_industry | multiple_recorded_industries",
    "largest_industry_count": "int"
  },
  "similarity_pattern": {
    "sample_size": "int",
    "top_5_sample_size": "int",
    "nearest_distance": "float or None",
    "average_distance_top_5": "float or None",
    "average_distance_top_10": "float or None",
    "gap_rank_1_to_rank_5": "float or None (requires 5 YC matches)"
  },
  "conclusion": "str, deterministic metadata summary and caution; no relevance classification"
}
```

Each Match has:

```json
{
  "id": "str",
  "source": "yc | user | unknown",
  "rank": "int (1-based within the query that returned it)",
  "company_name": "str",
  "short_description": "str (240 character display cap)",
  "document": "str (full stored document)",
  "industry": "str or None",
  "subindustry": "str or None",
  "batch": "str or None",
  "yc_url": "str or None",
  "metadata": "dict (unchanged)",
  "distance": "float (unchanged)"
}
```

## Rules and definitions

Top 10 overall results are retained verbatim under raw_retrieval.all_items. Top 10 real YC results are separately retrieved with the installed Chroma query(ids=...) API and retained under raw_retrieval.real_companies. A real YC item must have a yc: ID, company_id metadata and no source=user marker. User matches are identified through source=user. No database metadata is rewritten. A top-10 overall result can have a different rank from its YC-only rank; each rank is explicitly local to that retrieval.

Industry and subindustry counts use the actual recorded values; absent metadata is counted separately. Frequencies sort by descending count, then name, so ties are deterministic. Concentration is described through exact counts and single-versus-multiple recorded industries, with no arbitrary majority cutoff. Counts describe only the retrieved top 10, not the full market. Dataset categories are not normalized: a subindustry can look inconsistent with its industry.

Top-5 and top-10 averages use the actual distances. Gap is rank-5 distance minus rank-1 distance. Fewer available items use the actual sample size; the gap is None if there are fewer than five. Empty YC results return empty matches and None statistics. The closest_known_analog is only the first nearest YC vector; it is not an assertion of competition.

Reviewed previous examples: Onward ≈0.769, Cowlar ≈0.967, Hubble ≈1.059, Payflow ≈1.213 despite irrelevant higher-ranked results, and nonsense ≈1.726–1.794. They do not justify universal relevance thresholds. No hard relevance thresholds, percentages or sparse/very-similar labels were implemented. Named constants only control retrieval count (10), display count (5), and display excerpt length (240).

Conclusion wording reports the nearest retrieved YC result, exact metadata counts and the caveat that semantic neighbors are not verified competitors and this limited corpus cannot establish originality. It does not claim a query has any genuinely relevant match. This deliberately stays cautious even for nonsense.

## Actual query reports

### A — cattle monitoring

A device worn by cattle that warns ranchers when an animal may be ill or ready to breed.

Closest known analog (nearest YC vector): **Cowlar**, distance 0.96701580286026.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | Cowlar | 0.96701580286026 | Summary: Fitbit for dairy cows. Farms use cowlar's alerts & recommendations to… Tags: machine-learning; iot; agriculture Description: Cowlar, a fitbit for dairy cows provides data as a service to help dairy producers optimize operations… |

| 2 | Sendme, Inc | 1.2627296447753906 | Summary: On demand provider of meat to households and food businesses Tags: artificial-intelligence; e-commerce; food-tech Description: Sendme is an on-demand provider of clean meat to individuals and food businesses. We built a chatbot… |

| 3 | Vena Vitals | 1.3076263666152954 | Summary: A small sticker that monitors blood pressure continuously Tags: hard-tech; nanosensors; health-tech; medical-devices; digital-health Description: Vena Vitals makes a small sticker that monitors blood pressure continuously. We've… |

| 4 | Lifted | 1.320949912071228 | Summary: Smartwatch powered coaching to improve teams sustainable performance Tags: mental-health-tech; biometrics Description: NudgeLabs is a service that helps enterprises improve team performance and employee retention. We pair each… |

| 5 | Zeit Medical | 1.338008165359497 | Summary: Immediate stroke detection at home Tags: sleep-tech; consumer-health-services; medical-devices Description: Zeit Medical leverages the power of AI and wearable sensors to deliver peace of mind for those affected by stroke. Zeit’s… |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "Healthcare",
      "count": 5
    },
    {
      "name": "B2B",
      "count": 2
    },
    {
      "name": "Industrials",
      "count": 2
    },
    {
      "name": "Consumer",
      "count": 1
    }
  ],
  "subindustries": [
    {
      "name": "Healthcare -> Medical Devices",
      "count": 2
    },
    {
      "name": "B2B -> Human Resources",
      "count": 1
    },
    {
      "name": "B2B -> Productivity",
      "count": 1
    },
    {
      "name": "Consumer -> Food and Beverage",
      "count": 1
    },
    {
      "name": "Healthcare",
      "count": 1
    },
    {
      "name": "Healthcare -> Consumer Health and Wellness",
      "count": 1
    },
    {
      "name": "Healthcare -> Healthcare Services",
      "count": 1
    },
    {
      "name": "Industrials -> Agriculture",
      "count": 1
    },
    {
      "name": "Industrials -> Drones",
      "count": 1
    }
  ],
  "distinct_industries": 4,
  "distinct_subindustries": 9,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 5
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 0.96701580286026,
  "average_distance_top_5": 1.2392659783363342,
  "average_distance_top_10": 1.3007534801959992,
  "gap_rank_1_to_rank_5": 0.37099236249923706
}
```

Generated conclusion:

The nearest retrieved YC result is Cowlar (distance 0.967016). The 10 retrieved YC records span 4 recorded industries; the most frequent: Healthcare (5 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "Cowlar",
    "metadata": {
      "company_id": "1445",
      "subindustry": "Industrials -> Agriculture",
      "yc_url": "https://www.ycombinator.com/companies/cowlar",
      "company_name": "Cowlar",
      "industry": "Industrials",
      "batch": "Winter 2017",
      "status": "Inactive"
    }
  },
  {
    "rank": 2,
    "name": "Sendme, Inc",
    "metadata": {
      "industry": "Consumer",
      "yc_url": "https://www.ycombinator.com/companies/sendme-inc",
      "batch": "Winter 2022",
      "company_id": "25727",
      "company_name": "Sendme, Inc",
      "subindustry": "Consumer -> Food and Beverage",
      "status": "Active"
    }
  },
  {
    "rank": 3,
    "name": "Vena Vitals",
    "metadata": {
      "industry": "Healthcare",
      "company_name": "Vena Vitals",
      "company_id": "22206",
      "yc_url": "https://www.ycombinator.com/companies/vena-vitals",
      "batch": "Summer 2020",
      "subindustry": "Healthcare -> Medical Devices",
      "status": "Active"
    }
  },
  {
    "rank": 4,
    "name": "Lifted",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/lifted",
      "company_name": "Lifted",
      "status": "Active",
      "industry": "B2B",
      "subindustry": "B2B -> Human Resources",
      "company_id": "25357",
      "batch": "Winter 2022"
    }
  },
  {
    "rank": 5,
    "name": "Zeit Medical",
    "metadata": {
      "company_id": "24058",
      "yc_url": "https://www.ycombinator.com/companies/zeit-medical",
      "status": "Active",
      "industry": "Healthcare",
      "batch": "Summer 2021",
      "subindustry": "Healthcare -> Medical Devices",
      "company_name": "Zeit Medical"
    }
  }
]
```

### B — remote connectivity

Let small wireless gadgets send updates from remote areas where phones have no signal, through equipment orbiting Earth.

Closest known analog (nearest YC vector): **Doblet**, distance 1.0344176292419434.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | Doblet | 1.0344176292419434 | Summary: Doblet solves the phone battery problem. We're building the first… Tags: hardware Description: Doblet is the world’s first network of batteries on demand for charging phones everywhere. The company’s mission is to provide portable… |

| 2 | Hubble Network | 1.05861496925354 | Summary: Bluetooth to Space Tags: developer-tools; hard-tech; hardware; iot; satellites Description: Hubble is building a global satellite network that any Bluetooth-enabled device can connect to, even without cellular reception. Our… |

| 3 | Apolink | 1.0969836711883545 | Summary: 24/7 satellite connectivity in low Earth orbit Description: Apolink is building the world’s most interoperable satellite relay network in low Earth orbit. Our hybrid communication architecture combines RF and optical… |

| 4 | Toymail | 1.1929928064346313 | Summary: Connected toys that enable two-way voice messaging between children… Tags: iot; kids Description: The only kid-friendly WIFI toy messenger. Use our free app to message our toys from your phone & your child can reply right back!… |

| 5 | Wifi Dabba, Inc. | 1.2560151815414429 | Summary: Decentralised broadband connectivity. Tags: hardware; crypto-web3; telecommunications Description: We enable humans & machines with internet connectivity at a price that they can afford. The inspiration for Wifi Dabba came from… |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "Consumer",
      "count": 5
    },
    {
      "name": "Industrials",
      "count": 3
    },
    {
      "name": "B2B",
      "count": 1
    },
    {
      "name": "Healthcare",
      "count": 1
    }
  ],
  "subindustries": [
    {
      "name": "Consumer -> Consumer Electronics",
      "count": 3
    },
    {
      "name": "Industrials -> Aviation and Space",
      "count": 3
    },
    {
      "name": "B2B -> Office Management",
      "count": 1
    },
    {
      "name": "Consumer -> Home and Personal",
      "count": 1
    },
    {
      "name": "Consumer -> Social",
      "count": 1
    },
    {
      "name": "Healthcare -> Consumer Health and Wellness",
      "count": 1
    }
  ],
  "distinct_industries": 4,
  "distinct_subindustries": 6,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 5
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 1.0344176292419434,
  "average_distance_top_5": 1.1278048515319825,
  "average_distance_top_10": 1.2043716669082642,
  "gap_rank_1_to_rank_5": 0.2215975522994995
}
```

Generated conclusion:

The nearest retrieved YC result is Doblet (distance 1.034418). The 10 retrieved YC records span 4 recorded industries; the most frequent: Consumer (5 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "Doblet",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/doblet",
      "company_id": "667",
      "status": "Inactive",
      "company_name": "Doblet",
      "batch": "Summer 2014",
      "industry": "B2B",
      "subindustry": "B2B -> Office Management"
    }
  },
  {
    "rank": 2,
    "name": "Hubble Network",
    "metadata": {
      "batch": "Winter 2022",
      "industry": "Industrials",
      "yc_url": "https://www.ycombinator.com/companies/hubble-network",
      "company_name": "Hubble Network",
      "subindustry": "Industrials -> Aviation and Space",
      "company_id": "25313",
      "status": "Active"
    }
  },
  {
    "rank": 3,
    "name": "Apolink",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/apolink",
      "company_name": "Apolink",
      "status": "Active",
      "industry": "Industrials",
      "subindustry": "Industrials -> Aviation and Space",
      "company_id": "30130",
      "batch": "Fall 2024"
    }
  },
  {
    "rank": 4,
    "name": "Toymail",
    "metadata": {
      "batch": "Winter 2016",
      "status": "Inactive",
      "industry": "Consumer",
      "subindustry": "Consumer -> Consumer Electronics",
      "yc_url": "https://www.ycombinator.com/companies/toymail",
      "company_id": "1001",
      "company_name": "Toymail"
    }
  },
  {
    "rank": 5,
    "name": "Wifi Dabba, Inc.",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/wifi-dabba-inc",
      "status": "Active",
      "industry": "Consumer",
      "company_id": "1535",
      "subindustry": "Consumer -> Home and Personal",
      "batch": "Winter 2017",
      "company_name": "Wifi Dabba, Inc."
    }
  }
]
```

### C — meeting follow-up

Software that listens to meetings and automatically turns conversations into organized follow-up tasks.

Closest known analog (nearest YC vector): **Onward**, distance 0.7686163783073425.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | Onward | 0.7686163783073425 | Summary: Intelligent meeting automation for ambitious teams. Description: Onward is a new take on conversational intelligence. We streamline follow-ups, CRM updates, ticket creation, and other tasks after every meeting—helping you connect… |

| 2 | Fathom | 0.8351094722747803 | Summary: Never take notes again with the #1 AI Meeting Assistant Tags: saas; b2b Description: Instead of trying to hurriedly take notes while also having a conversation, you simply push a button in our app whenever you hear something… |

| 3 | DailyBot | 0.9807789325714111 | Summary: AI Assistant and Chat Add-ons for Work Tags: developer-tools; saas; collaboration; ai; ai-assistant Description: DailyBot is a chat AI Assistant and Workflow Automation platform. It takes chat to a new level by providing… |

| 4 | Moots AI | 0.9843339920043945 | Summary: Scan badges at business events, build context, and follow up with AI Tags: collaboration; social-network; crm; ai; ai-assistant Description: Going to trade shows or conferences? Moots AI helps you turn contacts into deals. We’re… |

| 5 | Findly | 1.0117197036743164 | Summary: Co-pilot for Business Intelligence Tags: artificial-intelligence; generative-ai; b2b; chatbot; data-engineering Description: Findly.ai is the co-pilot for Business Intelligence that revolutionizes how businesses understand and… |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "B2B",
      "count": 7
    },
    {
      "name": "Consumer",
      "count": 1
    },
    {
      "name": "Fintech",
      "count": 1
    },
    {
      "name": "Healthcare",
      "count": 1
    }
  ],
  "subindustries": [
    {
      "name": "B2B -> Productivity",
      "count": 4
    },
    {
      "name": "Fintech",
      "count": 2
    },
    {
      "name": "B2B -> Analytics",
      "count": 1
    },
    {
      "name": "B2B -> Operations",
      "count": 1
    },
    {
      "name": "B2B -> Sales",
      "count": 1
    },
    {
      "name": "Healthcare -> Consumer Health and Wellness",
      "count": 1
    }
  ],
  "distinct_industries": 4,
  "distinct_subindustries": 6,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 7
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 0.7686163783073425,
  "average_distance_top_5": 0.916111695766449,
  "average_distance_top_10": 0.9882753431797028,
  "gap_rank_1_to_rank_5": 0.24310332536697388
}
```

Generated conclusion:

The nearest retrieved YC result is Onward (distance 0.768616). The 10 retrieved YC records span 4 recorded industries; the most frequent: B2B (7 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "Onward",
    "metadata": {
      "batch": "Summer 2023",
      "industry": "B2B",
      "status": "Inactive",
      "subindustry": "B2B -> Productivity",
      "yc_url": "https://www.ycombinator.com/companies/onward",
      "company_name": "Onward",
      "company_id": "29124"
    }
  },
  {
    "rank": 2,
    "name": "Fathom",
    "metadata": {
      "company_name": "Fathom",
      "subindustry": "B2B -> Productivity",
      "status": "Active",
      "batch": "Winter 2021",
      "company_id": "22879",
      "industry": "B2B",
      "yc_url": "https://www.ycombinator.com/companies/fathom"
    }
  },
  {
    "rank": 3,
    "name": "DailyBot",
    "metadata": {
      "batch": "Summer 2021",
      "company_id": "24153",
      "company_name": "DailyBot",
      "subindustry": "B2B -> Productivity",
      "yc_url": "https://www.ycombinator.com/companies/dailybot",
      "status": "Active",
      "industry": "B2B"
    }
  },
  {
    "rank": 4,
    "name": "Moots AI",
    "metadata": {
      "batch": "Winter 2022",
      "company_name": "Moots AI",
      "subindustry": "B2B -> Productivity",
      "industry": "Consumer",
      "company_id": "25279",
      "status": "Active",
      "yc_url": "https://www.ycombinator.com/companies/moots-ai"
    }
  },
  {
    "rank": 5,
    "name": "Findly",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/findly",
      "status": "Active",
      "subindustry": "B2B -> Analytics",
      "industry": "B2B",
      "batch": "Summer 2022",
      "company_name": "Findly",
      "company_id": "27097"
    }
  }
]
```

### D — scattered work documents

A single place to find documents scattered across all the online services my team uses.

Closest known analog (nearest YC vector): **User Hero**, distance 1.1168444156646729.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | User Hero | 1.1168444156646729 | Summary: A hub for all your user research. Tags: saas; b2b; design-tools Description: User Hero collects all your user research in one place. Organize studies, transcribe interviews, take notes collaboratively, tag and search observations,… |

| 2 | Clew | 1.1465065479278564 | Summary: Unified file system for the cloud. Tags: saas; b2b Description: Clew lets employees see and organize files across their work apps from one place. |

| 3 | GoLinks | 1.1540071964263916 | Summary: Intuitive, easy-to-remember short links - powered by AI. Tags: saas; productivity; collaboration Description: GoLinks allows you to create internal links for your company that are so easy to remember and share, you don't have to… |

| 4 | AeroFS | 1.1861575841903687 | Summary: Secure Enterprise Collaboration. Tags: collaboration; security; enterprise Description: AeroFS enterprise file sync and share & collaboration solution deploys on your infrastructure. Your files remain secured by your own security… |

| 5 | Clarm | 1.1922050714492798 | Summary: Perplexity for internal docs Description: Clarm is your AI-native search and agent builder on internal docs. We are the #1 alignment meeting killer. Our first customers are delighted to pay us 10x less than they would spend on a… |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "B2B",
      "count": 9
    },
    {
      "name": "Consumer",
      "count": 1
    }
  ],
  "subindustries": [
    {
      "name": "B2B -> Engineering, Product and Design",
      "count": 3
    },
    {
      "name": "B2B -> Infrastructure",
      "count": 2
    },
    {
      "name": "B2B -> Finance and Accounting",
      "count": 1
    },
    {
      "name": "B2B -> Office Management",
      "count": 1
    },
    {
      "name": "B2B -> Productivity",
      "count": 1
    },
    {
      "name": "B2B -> Recruiting and Talent",
      "count": 1
    },
    {
      "name": "Consumer -> Content",
      "count": 1
    }
  ],
  "distinct_industries": 2,
  "distinct_subindustries": 7,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 9
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 1.1168444156646729,
  "average_distance_top_5": 1.1591441631317139,
  "average_distance_top_10": 1.1989997982978822,
  "gap_rank_1_to_rank_5": 0.07536065578460693
}
```

Generated conclusion:

The nearest retrieved YC result is User Hero (distance 1.116844). The 10 retrieved YC records span 2 recorded industries; the most frequent: B2B (9 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "User Hero",
    "metadata": {
      "industry": "B2B",
      "company_name": "User Hero",
      "batch": "Summer 2018",
      "yc_url": "https://www.ycombinator.com/companies/user-hero",
      "status": "Inactive",
      "company_id": "1890",
      "subindustry": "B2B -> Engineering, Product and Design"
    }
  },
  {
    "rank": 2,
    "name": "Clew",
    "metadata": {
      "batch": "Summer 2020",
      "industry": "B2B",
      "status": "Acquired",
      "company_id": "21997",
      "company_name": "Clew",
      "yc_url": "https://www.ycombinator.com/companies/clew",
      "subindustry": "B2B -> Infrastructure"
    }
  },
  {
    "rank": 3,
    "name": "GoLinks",
    "metadata": {
      "industry": "B2B",
      "yc_url": "https://www.ycombinator.com/companies/golinks",
      "company_id": "11984",
      "status": "Active",
      "batch": "Winter 2019",
      "company_name": "GoLinks",
      "subindustry": "B2B -> Productivity"
    }
  },
  {
    "rank": 4,
    "name": "AeroFS",
    "metadata": {
      "subindustry": "B2B -> Infrastructure",
      "company_name": "AeroFS",
      "yc_url": "https://www.ycombinator.com/companies/aerofs",
      "industry": "B2B",
      "company_id": "183",
      "batch": "Summer 2010",
      "status": "Acquired"
    }
  },
  {
    "rank": 5,
    "name": "Clarm",
    "metadata": {
      "status": "Active",
      "subindustry": "B2B -> Finance and Accounting",
      "industry": "B2B",
      "batch": "Spring 2025",
      "company_name": "Clarm",
      "yc_url": "https://www.ycombinator.com/companies/clarm",
      "company_id": "30439"
    }
  }
]
```

### Nonsense

Quantum marshmallow nebula dances inside a purple theorem.

Closest known analog (nearest YC vector): **Zenflow**, distance 1.7256138324737549.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | Zenflow | 1.7256138324737549 | Summary: Medical device that provides a more effective, less invasive… Tags: medical-devices Description: Forty million men in the US and over 500 million worldwide suffer from urinary obstruction related to benign prostatic hyperplasia… |

| 2 | Turion Space | 1.7364881038665771 | Summary: Moving Things Around in Space, Imaging Space Objects When We're Not Tags: space-exploration; satellites Description: Turion Space is building spacecraft to move things around in space and image space objects when they’re not, and… |

| 3 | SlidePay | 1.7375915050506592 | Summary: Banking and Payment Platform APIs. Exited October 2014. Tags: fintech; payments; api Description: SlidePay, formerly Cube, is an API that makes it easy for any app to accept credit cards that are processed in person. Integration… |

| 4 | Hubble Network | 1.7415380477905273 | Summary: Bluetooth to Space Tags: developer-tools; hard-tech; hardware; iot; satellites Description: Hubble is building a global satellite network that any Bluetooth-enabled device can connect to, even without cellular reception. Our… |

| 5 | Clew | 1.766330361366272 | Summary: Unified file system for the cloud. Tags: saas; b2b Description: Clew lets employees see and organize files across their work apps from one place. |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "Consumer",
      "count": 3
    },
    {
      "name": "Industrials",
      "count": 3
    },
    {
      "name": "B2B",
      "count": 2
    },
    {
      "name": "Fintech",
      "count": 1
    },
    {
      "name": "Healthcare",
      "count": 1
    }
  ],
  "subindustries": [
    {
      "name": "Industrials -> Aviation and Space",
      "count": 3
    },
    {
      "name": "B2B -> Infrastructure",
      "count": 2
    },
    {
      "name": "Consumer -> Content",
      "count": 2
    },
    {
      "name": "Consumer -> Home and Personal",
      "count": 1
    },
    {
      "name": "Fintech -> Payments",
      "count": 1
    },
    {
      "name": "Healthcare -> Medical Devices",
      "count": 1
    }
  ],
  "distinct_industries": 5,
  "distinct_subindustries": 6,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 3
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 1.7256138324737549,
  "average_distance_top_5": 1.741512370109558,
  "average_distance_top_10": 1.7635316848754883,
  "gap_rank_1_to_rank_5": 0.04071652889251709
}
```

Generated conclusion:

The nearest retrieved YC result is Zenflow (distance 1.725614). The 10 retrieved YC records span 5 recorded industries; the most frequent: Consumer, Industrials (3 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "Zenflow",
    "metadata": {
      "subindustry": "Healthcare -> Medical Devices",
      "company_id": "834",
      "batch": "Winter 2015",
      "status": "Active",
      "industry": "Healthcare",
      "company_name": "Zenflow",
      "yc_url": "https://www.ycombinator.com/companies/zenflow"
    }
  },
  {
    "rank": 2,
    "name": "Turion Space",
    "metadata": {
      "status": "Active",
      "company_name": "Turion Space",
      "yc_url": "https://www.ycombinator.com/companies/turion-space",
      "batch": "Summer 2021",
      "industry": "Industrials",
      "subindustry": "Industrials -> Aviation and Space",
      "company_id": "24865"
    }
  },
  {
    "rank": 3,
    "name": "SlidePay",
    "metadata": {
      "company_id": "20",
      "industry": "Fintech",
      "yc_url": "https://www.ycombinator.com/companies/slidepay",
      "company_name": "SlidePay",
      "batch": "Winter 2012",
      "subindustry": "Fintech -> Payments",
      "status": "Acquired"
    }
  },
  {
    "rank": 4,
    "name": "Hubble Network",
    "metadata": {
      "industry": "Industrials",
      "batch": "Winter 2022",
      "subindustry": "Industrials -> Aviation and Space",
      "company_name": "Hubble Network",
      "status": "Active",
      "company_id": "25313",
      "yc_url": "https://www.ycombinator.com/companies/hubble-network"
    }
  },
  {
    "rank": 5,
    "name": "Clew",
    "metadata": {
      "subindustry": "B2B -> Infrastructure",
      "company_id": "21997",
      "company_name": "Clew",
      "yc_url": "https://www.ycombinator.com/companies/clew",
      "status": "Acquired",
      "industry": "B2B",
      "batch": "Summer 2020"
    }
  }
]
```

### User-item separation

Help ocean ecologists spot stressed or unhealthy stony sea organisms being regrown, using submerged imaging and automatic warnings.

Closest known analog (nearest YC vector): **Industrial Microbes**, distance 1.3699941635131836.

| Rank | Company | Distance | Short description |
|---|---|---:|---|

| 1 | Industrial Microbes | 1.3699941635131836 | Summary: We design and build microbes to make chemicals greener at lower cost. Tags: carbon-capture-and-removal; bioplastic; climate Description: At iMicrobes, we believe there are opportunities for biology to solve our biggest problems.… |

| 2 | MantleBio | 1.4502487182617188 | Summary: Transform scientific data into discoveries Tags: saas; biotech; data-science Description: Mantle brings modern data engineering to the lab to help scientists turn insights into world-changing breakthroughs. |

| 3 | Invert | 1.4815195798873901 | Summary: Data analytics software for biomanufacturing. Tags: cellular-agriculture; machine-learning; synthetic-biology; biotech Description: We build software to manage, analyze, and optimize bioprocessing data. Our initial customers are… |

| 4 | Spect | 1.4848089218139648 | Summary: Value-based retinal screening in primary care to prevent blindness. Tags: digital-health; ai Description: Vision Disease cause innumerable cases of preventable blindness globally - 415 million diabetic patients worldwide are… |

| 5 | SpecCheck | 1.4901938438415527 | Summary: Unifying how the optical industry does business. Tags: saas; payments; health-tech; b2b; api Description: SpecCheck is an all-in-one solution that provides accurate prescription eyewear ordering and tracking, seamless billing, and… |

Market neighborhood (computed from top 10 YC records):

```json
{
  "sample_size": 10,
  "industries": [
    {
      "name": "Healthcare",
      "count": 6
    },
    {
      "name": "B2B",
      "count": 2
    },
    {
      "name": "Industrials",
      "count": 2
    }
  ],
  "subindustries": [
    {
      "name": "B2B",
      "count": 2
    },
    {
      "name": "Healthcare -> Consumer Health and Wellness",
      "count": 2
    },
    {
      "name": "Healthcare -> Industrial Bio",
      "count": 2
    },
    {
      "name": "Healthcare",
      "count": 1
    },
    {
      "name": "Healthcare -> Medical Devices",
      "count": 1
    },
    {
      "name": "Industrials -> Climate",
      "count": 1
    },
    {
      "name": "Industrials -> Energy",
      "count": 1
    }
  ],
  "distinct_industries": 3,
  "distinct_subindustries": 7,
  "missing_industry_count": 0,
  "missing_subindustry_count": 0,
  "distribution": "multiple_recorded_industries",
  "largest_industry_count": 6
}
```

Similarity pattern:

```json
{
  "sample_size": 10,
  "top_5_sample_size": 5,
  "nearest_distance": 1.3699941635131836,
  "average_distance_top_5": 1.455353045463562,
  "average_distance_top_10": 1.4941986203193665,
  "gap_rank_1_to_rank_5": 0.12019968032836914
}
```

Generated conclusion:

The nearest retrieved YC result is Industrial Microbes (distance 1.369994). The 10 retrieved YC records span 3 recorded industries; the most frequent: Healthcare (6 records each). These are nearest semantic neighbors, not verified competitors; this limited corpus cannot establish originality.

Metadata for top 5:

```json
[
  {
    "rank": 1,
    "name": "Industrial Microbes",
    "metadata": {
      "subindustry": "Healthcare -> Industrial Bio",
      "industry": "Healthcare",
      "batch": "Winter 2015",
      "company_name": "Industrial Microbes",
      "yc_url": "https://www.ycombinator.com/companies/industrial-microbes",
      "status": "Active",
      "company_id": "813"
    }
  },
  {
    "rank": 2,
    "name": "MantleBio",
    "metadata": {
      "yc_url": "https://www.ycombinator.com/companies/mantlebio",
      "batch": "Summer 2023",
      "status": "Inactive",
      "company_name": "MantleBio",
      "subindustry": "B2B",
      "industry": "B2B",
      "company_id": "28967"
    }
  },
  {
    "rank": 3,
    "name": "Invert",
    "metadata": {
      "industry": "Healthcare",
      "company_name": "Invert",
      "status": "Active",
      "subindustry": "Healthcare -> Industrial Bio",
      "yc_url": "https://www.ycombinator.com/companies/invert",
      "batch": "Winter 2022",
      "company_id": "25399"
    }
  },
  {
    "rank": 4,
    "name": "Spect",
    "metadata": {
      "status": "Active",
      "yc_url": "https://www.ycombinator.com/companies/spect",
      "industry": "Healthcare",
      "company_name": "Spect",
      "subindustry": "Healthcare -> Consumer Health and Wellness",
      "batch": "Summer 2017",
      "company_id": "1641"
    }
  },
  {
    "rank": 5,
    "name": "SpecCheck",
    "metadata": {
      "subindustry": "B2B",
      "status": "Active",
      "company_id": "28413",
      "company_name": "SpecCheck",
      "industry": "B2B",
      "yc_url": "https://www.ycombinator.com/companies/speccheck",
      "batch": "Winter 2023"
    }
  }
]
```

User-created matches are separate (ranks among overall results):

```json
[
  {
    "id": "user:8a87d2f9-c8f8-429e-bc17-c79259264faa",
    "source": "user",
    "rank": 1,
    "company_name": "Development test \u2014 Reef Nursery Monitor",
    "short_description": "An underwater camera system watches coral restoration nurseries, detects bleaching and disease in reef fragments, and alerts marine conservation teams when colonies need treatment.",
    "document": "An underwater camera system watches coral restoration nurseries, detects bleaching and disease in reef fragments, and alerts marine conservation teams when colonies need treatment.",
    "industry": null,
    "subindustry": null,
    "batch": null,
    "yc_url": null,
    "metadata": {
      "source": "user",
      "company_name": "Development test \u2014 Reef Nursery Monitor"
    },
    "distance": 0.8465203046798706
  }
]
```

## Observed quality and checks

Cowlar remained #1, Hubble Network #2, and Onward #1. Doblet still outranked Hubble despite being a phone-charging service; neutral rank-1 labeling does not repair semantic errors. D uses the separate realistic work-document aggregation concept: User Hero is nearest, while Clew at #2 more directly fits files across apps. No corpus changes were made to force matches.

Nonsense returns Zenflow as nearest with distance 1.7256138324737549. Its top-5 mean is 1.741512370109558 and top-10 mean is 1.7635316848754883. Its small rank-1/rank-5 gap (0.04071652889251709) does not establish relevance. The same caution is included in every generated conclusion; no competitor claim is emitted.

Tested exact arithmetic on fixture distances, missing metadata counts, source separation, empty results, fewer than five matches and invalid input. Ran analyze_idea on A-D, nonsense and the existing user paraphrase, twice per query to check deterministic equality. Verified all raw distances survive cleaning and top-10 means match actual results. Verified that a rank-1 user match coexists with ten real company matches. No new user record was inserted.

Fingerprints of all 1001 yc_startups IDs/documents/metadata/embedding vectors and all 10 startup_ideas records were identical before and after analysis. Count remains 1001 (1000 real YC records plus 1 user item). Actual JSON reports, including complete raw Chroma output, are saved in ignored data/analysis_results.json. Run python3 verify_analysis.py to reproduce the checks.

An initial environment probe without elevated filesystem permission encountered a readonly-database error because the standalone directory is outside the default writable workspace. The authorized elevated verification runs succeeded; there were no analysis-function or verification failures. Nothing was committed or pushed. No final CLI, frontend, deployment or README was created.
