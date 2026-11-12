# Where to search, by field: repositories, portals and archives

This is a map of where data of a given kind is held. It is for searches beyond the five registries the CLI already covers (OpenAIRE, DataCite, Zenodo, Hugging Face Hub, PhysioNet). Many repositories below also register DataCite DOIs, so a DataCite hit may already point into one of them. It names repositories only, never datasets.
How to use it: (1) pick every field the question touches; (2) search each portal's own search page or API with the user's terms (use `site:` web searches where there is no API); (3) take the access conditions from each dataset's own landing page. The "Typical access" column is only the usual pattern, and at most portals access varies by dataset. (4) Rows marked *catalogue* hold metadata only, so confirm the dataset on the repository that actually holds it.
Access words follow the SPEC tiers: `open` (direct download), `account` (free login or click-through terms), `gated` (application, credentialing or owner approval), `controlled` (institutional agreement, ethics approval, access committee, fee or secure enclave).
Checked 2026-11-11. The status in brackets is from a request made that day: "blocked" means the site refused automated clients, "answered" means an API call returned data, and **UNVERIFIED** means the point could not be confirmed on the repository's own pages that day (the re3data record is quoted as a cross-check where one exists).

### 1. Clinical and hospital records
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| PhysioNet (also field 2) | https://physionet.org/ (200) | Physiological signals, structured EHR, clinical text, imaging | Per project: open; restricted (registered user + data use agreement); credentialed (credentialing + training + DUA) | Search page; already searched by the CLI | Read the access policy on each project page |
| HDR UK Health Data Research Gateway | https://healthdatagateway.org/en (200) | *Catalogue* of UK health datasets held by data custodians | Holds no data. Access is requested from each custodian (`controlled`); it is the front door to the NHS Research Secure Data Environment network | Search page; API docs at https://api.healthdatagateway.org/api/documentation (200) | Metadata only; the custodian decides |
| EHDEN | https://www.ehden.eu/ (200); portal https://portal.ehden.eu/ (timed out today) | *Catalogue* of 100+ European data sources mapped to the OMOP common data model (metadata, record counts) | Portal needs an account. No patient-level download is offered; how studies are run with data partners is UNVERIFIED | Data Partner Catalogue | Counts and metadata only |
| ResDAC (CMS research data) | https://resdac.org/ (200 to a browser client, intermittent timeouts) | US Medicare and Medicaid claims and enrolment research files | `controlled`: request for identifiable files under the CMS policy guide, IRB requirements and CMS fees; a virtual research data center (enclave) is offered | Request guidance; no data API stated | US federal process; fees |

### 2. Physiological signals and biosignals (see also PhysioNet in 1, OpenNeuro and DANDI in 4)
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| National Sleep Research Resource | https://sleepdata.org/ (TLS chain not verifiable by curl or WebFetch; exists per https://www.re3data.org/api/v1/repository/r3d100011861) | Sleep data: polysomnography, actigraphy, questionnaires (from re3data) | UNVERIFIED (re3data: open plus registration-restricted) | UNVERIFIED | Some clients reject its certificate; open it in a browser |
| Neural Engineering Data Consortium | https://isip.piconepress.com/projects/nedc/ (200) | Clinical EEG corpora; digital pathology images | `gated`: email a signed request form; credentials are sent after acceptance; download via ssh keys and rsync | Corpus pages; no API | Manual approval by e-mail |
| BNCI Horizon 2020 database | https://bnci-horizon-2020.eu/database/data-sets (200) | Brain-computer-interface recordings (EEG, ECoG, fNIRS) | `open`: direct download under each entry's Creative Commons licence | One list page; no API | Cite the linked publication |
| IEEE DataPort | https://ieee-dataport.org/ (200) | Engineering datasets of all kinds, including biosignals and sensors | Open-access files need a free login; other datasets need a subscription | Dataset search; API not stated | Uploads by users; licences vary |

### 3. Medical imaging
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| The Cancer Imaging Archive (TCIA) | https://www.cancerimagingarchive.net/ (200) | De-identified cancer imaging (DICOM radiology, pathology) | Public download after agreeing to its Data Usage Policies; some collections restricted (re3data: registration) | Site search; public query API; download tools | Check each collection's licence |
| NCI Imaging Data Commons (IDC) | https://portal.imaging.datacommons.cancer.gov/ (200) | Cancer radiology, pathology and microscopy images with derived and clinical data | `open`: no registration and no access requests; public Google and AWS buckets | Web portal; BigQuery; `idc-index` Python package; S3 clients | Over 95% CC BY, a small part non-commercial |
| MIDRC | https://www.midrc.org/ (200); data portal https://data.midrc.org/ (timed out today) | Medical images and metadata received through the RSNA and ACR intake portals | `account`: open to registered users under its data use agreement | Data portal; federated imaging hub | Registration and DUA first |
| Stanford AIMI shared data | https://aimi.stanford.edu/data (200, redirected from /shared-datasets) | Imaging, clinical text, structured health data, annotations | Free for non-commercial research; per-dataset requirements; delivered through Redivis | Dataset index page | Commercial use needs a separate licence |
| Grand Challenge | https://grand-challenge.org/challenges/ (200) | Index of biomedical image-analysis challenges | Varies by challenge: an account; some challenges require a signed data agreement and organiser approval | Filterable challenge list | Terms are set per challenge |

### 4. Neuroscience and brain imaging
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| OpenNeuro | https://openneuro.org/ (200) | Shared neuroimaging data | `open` for public datasets: CLI, git/DataLad, public S3 bucket (anonymous listing answered) | Search page; GraphQL API | Licence per dataset UNVERIFIED |
| DANDI Archive | https://dandiarchive.org/ (200) | Neurophysiology data (NWB standard) | `open` for public dandisets (REST API answered anonymously); embargoed dandisets exist (re3data) | Search; REST API; DANDI client | None noted |
| NIMH Data Archive (NDA) | https://nda.nih.gov/ (200, JavaScript app) | Human mental-health research data | `controlled`, free of charge: NDA account, Data Access Request and Data Use Certification signed by the institution | Query tools (UNVERIFIED) | Requires an NIH-recognised institution (eRA registration) with an active Federalwide Assurance |
| EBRAINS Knowledge Graph | https://search.kg.ebrains.eu/ (200) | Neuroscience data, models and software across species and modalities | Most data `open`; sensitive human data need an EBRAINS account and a data use agreement (UNVERIFIED, wiki seen only in search results) | KG search with filters; KG API (EBRAINS account) | None noted |
| LONI Image and Data Archive | https://ida.loni.usc.edu/ (200) | Neuroimaging studies with clinical and genetic data | Open Use studies need an IDA account; other studies need an application to that study | Per-study pages after login | Some study pages are restricted by their PIs |

### 5. Genomics and other omics, including controlled-access human data
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| NCBI GEO | https://www.ncbi.nlm.nih.gov/geo/ (200; web pages showed a browser check to scripts) | Functional genomics (expression, methylation and other array or sequencing data) | `open` (FTP directory answered without login) | E-utilities API (answered); FTP | Use E-utilities, not page scraping |
| European Nucleotide Archive (ENA) | https://www.ebi.ac.uk/ena/browser/home (200) | Nucleotide sequences, raw reads, assemblies, analyses | `open` (re3data: open) | Portal API (answered anonymously); FTP | Raw read files are large; filter with the API first |
| dbGaP | https://dbgap.ncbi.nlm.nih.gov/home/ (200) | Human genotype-phenotype studies | Study pages and public files open; individual-level data via Authorized Access under the NIH request policy (`controlled`) | Advanced public search | Detailed steps not on its home page (GDC's page names dbGaP authorization and eRA Commons login) |
| European Genome-phenome Archive (EGA) | https://ega-archive.org/ (200) | Personally identifiable human genetic and phenotypic data | `controlled`: EGA account, then a request per dataset to its Data Access Committee (contact the DAC by e-mail too) | Search; DAC catalogue | Policies vary even within one DAC |
| NBDC Human Database / JGA (Japan) | https://humandbs.dbcls.jp/en/ (200); https://www.ddbj.nig.ac.jp/jga/index-e.html (200) | Japanese human genomic and phenotype data | Summaries open; controlled data need a DDBJ account and an application to DBCLS; JGA grants access after approval | Research and dataset lists | Site notes a review backlog |
| NCI Genomic Data Commons (GDC) | https://portal.gdc.cancer.gov/ (200) | Cancer genomic, clinical and biospecimen data | Open tier with no login; controlled tier needs dbGaP authorization and eRA Commons login | Data portal; REST API (answered); transfer tool | Low-level sequence and germline data are controlled |
| ProteomeXchange | https://proteomecentral.proteomexchange.org/ (200) | Mass-spectrometry proteomics from member repositories (PRIDE, PeptideAtlas, MassIVE, jPOST, iProX) | Public datasets are open from the member repository (re3data: open, restricted) | ProteomeCentral browse; RSS | Files live in the member repository |

### 6. Public health, epidemiology and population health surveys
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| CDC open data portal | https://data.cdc.gov/ (200) | US public-health surveillance and statistics tables | `open` | Search; Socrata API (metadata endpoint answered) | Check each table's own notes |
| WHO Global Health Observatory | https://www.who.int/data/gho (200) | Country-level health indicators | `open` | GHO OData API (answered) | Indicators, not microdata |
| IHME GHDx | https://ghdx.healthdata.org/ (200) | *Catalogue* of surveys, censuses, vital statistics and other health data, plus IHME results | IHME downloads are free for non-commercial use under its user agreement; other entries point to their providers | Catalogue search | Commercial use needs an IHME enquiry |
| The DHS Program | https://dhsprogram.com/data/ (200) | Household survey microdata (surveys, HIV, GPS), many countries | `gated`: registered user and project description; approval is per country, usually within days; extra terms for GPS and biomarker data | Download by survey; API https://api.dhsprogram.com/rest/dhs/countries?f=json (answered) | No passing data on without written consent |
| Maelstrom Catalogue | https://www.maelstrom-research.org/ (200) | *Catalogue* of epidemiological studies, networks, variables and harmonisation | Metadata only (page does not say it hosts data); access route per study UNVERIFIED | Study, network and variable search | Contact each study for its data |

### 7. Clinical trials data sharing platforms
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| Vivli | https://vivli.org/ (200) | Participant-level trial data from member contributors | `controlled`: account, data request form (team needs a qualified statistician), review, data-access training and DUA; analysis in Vivli's secure research environment | Study search | Team members at other institutions each sign the DUA |
| YODA Project | https://yoda.yale.edu/ (200) | Trial data from industry data partners | `controlled`: YODA reviews each request; DUA training; access on a secure platform (UNVERIFIED) | Trial listings | None noted |
| ClinicalStudyDataRequest.com | https://clinicalstudydatarequest.com/ (200; the www host did not answer) | Patient-level data from a consortium of trial sponsors | Search needs no account; account plus research proposal to request (`controlled`) | Study search | Use the bare domain |
| Project Data Sphere | https://data.projectdatasphere.org/projectdatasphere/html/home (200, JavaScript app) | De-identified patient-level data from cancer phase II-III trials (from re3data) | UNVERIFIED (re3data: registration) | UNVERIFIED | Site did not render to automated clients |
| NHLBI BioLINCC | https://biolincc.nhlbi.nih.gov/home/ (200) | Data and biospecimens from NHLBI-funded studies and trials | Account with identity check (Login.gov in the US, ID.me outside), request and data use agreement (`controlled`) | Study pages | Non-US users must verify through ID.me |

### 8. Social science and survey archives
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| ICPSR | https://www.icpsr.umich.edu/ (403, blocked; exists per https://www.re3data.org/api/v1/repository/r3d100010255) | Social and behavioural science data archive (from re3data) | UNVERIFIED (re3data: open, registration, fee-required and closed tiers) | UNVERIFIED | Blocked to scripts; search it in a browser |
| UK Data Service | https://ukdataservice.ac.uk/ (200) | UK and international survey, census, longitudinal and administrative data | Open (no registration); safeguarded (register and accept the End User Licence); controlled (application, SecureLab TRE, approved device or Safe Room) | Catalogue search; OAI-PMH (re3data) | Controlled data only for experienced, approved researchers |
| CESSDA Data Catalogue | https://datacatalogue.cessda.eu/ (200, JavaScript app) | *Catalogue* of 40,000+ collections held by CESSDA service providers in 20+ European countries | Data come from each provider under its terms | Search page; API UNVERIFIED (re3data: OAI-PMH, REST) | Metadata in providers' languages |
| SSJDA (University of Tokyo) | https://csrda.iss.u-tokyo.ac.jp/ (200) | Japanese social survey microdata | `gated`: online application through SSJDA Direct; limits on the number of applications | Data search; online analysis | Eligibility rules UNVERIFIED |
| IPUMS | https://www.ipums.org/ (403, blocked); https://usa.ipums.org/usa/ (200) | Harmonised census and survey microdata from around the world | `account`: free registration and agreement to the terms of use | Extract builder; IPUMS API https://developer.ipums.org/ (200) | Redistribution is limited |

### 9. Economics and official statistics
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| World Bank Open Data and Microdata Library | https://data.worldbank.org/ (200); https://microdata.worldbank.org/ (200) | Development indicators; household and enterprise survey microdata | Indicators `open`. Microdata per dataset: direct (no login), public use (accept terms), licensed (application and signed agreement), or external host | Indicators API (answered); microdata search | External microdata carry the owner's terms |
| IMF Data | https://data.imf.org/ (403, blocked; WebFetch saw sign-in and API links) | Macroeconomic and financial statistics | Portal terms UNVERIFIED | SDMX 2.1 API https://api.imf.org/external/sdmx/2.1/dataflow (answered) | Portal blocks scripts; use the API |
| OECD Data Explorer | https://data-explorer.oecd.org/ (200) | OECD economic and social statistics | Web explorer; terms UNVERIFIED (oecd.org pages blocked) | SDMX API https://sdmx.oecd.org/public/rest/dataflow/all?detail=allstubs (answered anonymously) | oecd.org pages block scripts |
| Eurostat | https://ec.europa.eu/eurostat/data/database (200) | EU official statistics; confidential microdata | Aggregates `open` with a free REST API. Microdata `controlled`: organisation recognised as a research entity, then a research proposal (about 8-10 weeks) | Database browser; REST API (catalogue answered) | Microdata for scientific purposes only |
| e-Stat (Japan) | https://www.e-stat.go.jp/en (200) | Japanese government statistics | Web download; API needs e-Stat registration (`account`) | Search; e-Stat API | Open web-download terms UNVERIFIED |
| Office for National Statistics (UK) | https://www.ons.gov.uk/ (200) | UK official statistics | Published data `open`; de-identified unpublished data via the Secure Research Service, for accredited researchers | Site search; open API with no key, https://api.beta.ons.gov.uk/v1/datasets (answered) | API is in beta |
| US Census Bureau | https://data.census.gov/ (200) | US census and survey tables and microdata | Public tables and API `open`; restricted-use microdata only in Federal Statistical Research Data Centers after a proposal | data.census.gov; Census Data API (catalogue answered) | Restricted-use work is in secure centres |

### 10. Earth observation, climate and environment
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| NASA Earthdata | https://www.earthdata.nasa.gov/ (200) | NASA Earth-science data from its archive centres (DAACs) | `account`: Earthdata Login registration to get data from the DAACs | Earthdata Search; CMR API (answered) | Each archive centre has its own tools |
| Copernicus Data Space Ecosystem | https://dataspace.copernicus.eu/ (200) | Copernicus satellite products and service datasets | Register (accept the terms) and log in for services; whether plain downloads need login UNVERIFIED | Browser; OData catalogue and STAC (answered); openEO | Quotas exist (link seen, not read) |
| Copernicus Climate Data Store | https://cds.climate.copernicus.eu/ (200) | Climate reanalyses, projections and observations | `account`: register and log in; the API needs a personal access token | Catalogue search; `cdsapi` client | Site notice about protection measures that limit downloads |
| NOAA NCEI | https://www.ncei.noaa.gov/ (200) | Weather, climate, ocean and geophysical archives | `open`: direct download (csv, bulk, shapefile) | Data Access app; Search API (answered) | Cloud migration may delay access |
| Earth System Grid Federation | https://esgf.github.io/ (200); search https://metagrid.esgf-west.org/search (200, JavaScript app) | Distributed climate model output | Download without joining a project; some data in access-control groups (legacy user guide) | Metagrid search (beta); wget scripts; OPeNDAP | Federation in transition; OpenID logins fail on some legacy nodes |
| PANGAEA | https://www.pangaea.de/ (200) | Georeferenced earth and environmental science data | `open` under each dataset's licence; a few datasets under moratorium | Search; OAI-PMH (answered) | Moratorium datasets are not yet public |

### 11. Agriculture and food
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| FAOSTAT | https://www.fao.org/faostat/en/ (200, JavaScript app) | Food and agriculture statistics by country | `open`: FAO statistical databases are CC BY 4.0 unless stated (FAO terms of use) | Web app; API UNVERIFIED | Some third-party data may not be redistributed |
| FAO Food and Agriculture Microdata Catalogue | https://microdata.fao.org/ (200) | About 1,800 agricultural and food survey microdata records | Per dataset; licensed files need a named lead researcher and a signed agreement | Catalogue search | Destroy data after the research; send outputs to FAO |
| USDA NASS Quick Stats | https://quickstats.nass.usda.gov/ (200) | US agricultural statistics | `open` web queries; API key by e-mail after accepting the terms | Query tool; API; bulk files | 50,000 records per API call |
| USDA Ag Data Commons | https://www.nal.usda.gov/services/agdatacommons (200, redirected from data.nal.usda.gov) | Catalogue and repository for USDA-funded research data | `open` (public-access data only, no PII) | Catalogue search; API UNVERIFIED | Many records point to other hosts |
| CGIAR GARDIAN | https://gardian.cgiar.org/ (200, JavaScript app) | Harvester of publications and datasets from CGIAR centres' repositories | Access set by each source repository (UNVERIFIED) | Search page | Described from https://bigdata.cgiar.org/resources/gardian/ (200) |

### 12. Energy
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| US EIA Open Data | https://www.eia.gov/opendata/ (200) | US energy production, consumption and prices | `open`; the API needs a key sent by e-mail; bulk download needs no key | API v2; bulk download | None noted |
| IEA Data and statistics | https://www.iea.org/data-and-statistics (200) | Global energy statistics | Mixed: free datasets need a free IEA account; others are paid subscriptions | Data browser | Free and paid datasets sit side by side |
| ENTSO-E Transparency Platform | https://transparency.entsoe.eu/ (200, JavaScript app) | European electricity generation, load, transmission and market data | UNVERIFIED: registration, then an API token requested by e-mail (help-centre page blocked; seen only in search results) | REST API (UNVERIFIED) | Help centre blocks scripts |
| Open Energy Data Initiative (OEDI) | https://data.openei.org/ (200) | US DOE energy datasets and cloud data lakes | `open` access | Search; API UNVERIFIED (re3data: REST, SPARQL) | None noted |
| IRENA statistics | https://www.irena.org/Data (200 to curl; 403 to WebFetch) | Renewable capacity, generation and energy balances reported by members | UNVERIFIED | UNVERIFIED | Blocks some clients |

### 13. Transport and mobility
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| US DOT Open Data Portal | https://data.transportation.gov/ (200) | US transport datasets, including Bureau of Transportation Statistics tables | `open` | Search; Socrata API (metadata endpoint answered) | bts.gov answered 403 to scripts |
| Mobility Database | https://mobilitydatabase.org/ (200) | Catalogue of 6,000+ GTFS, GTFS-Realtime and GBFS feeds from 100+ countries | Free browsing and download; the API needs a free account | Search; map preview; API | Feeds come from third-party producers |
| Transitland | https://www.transit.land/ (200) | Transit feed registry and archive of GTFS feeds since 2015 | Website free to browse; APIs need a key (401 without one), free to start, then metered | REST and GraphQL APIs | Metered pricing; separate commercial plans |
| ODPT (Japan) | https://www.odpt.org/ (200); https://developer.odpt.org/ (200) | Japanese public transport data | `account`: free user registration, then the API | API spec on the developer site | Japanese-language site |

### 14. Language, text and speech corpora
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| Linguistic Data Consortium (LDC) | https://catalog.ldc.upenn.edu/ (200) | Hundreds of speech, text and lexical corpora | Annual for-profit or not-for-profit membership, or per-corpus licence; non-member terms UNVERIFIED | Catalog search | ldc.upenn.edu info pages answered 403 |
| ELRA Catalogue | https://catalog.elra.info/en-us/ (200) | Speech, text, lexical and terminology resources | Purchase: price depends on ELRA membership, organisation type and licence (research or commercial) | Search and browse | Prices differ by licence and membership |
| CLARIN Virtual Language Observatory | https://vlo.clarin.eu/ (200; proof-of-work bot check) | *Catalogue* of hundreds of thousands of language resources | Availability levels Public, Academic, Restricted; files come from the source repository | Faceted search | Bot check blocks scripts |
| OpenSLR | https://www.openslr.org/ (200) | Speech and language resources for training | `open`: browser or wget download | Index pages | Download one file at a time |
| NII Informatics Research Data Repository | https://www.nii.ac.jp/dsc/idr/en/ (200) | Datasets offered by companies and institutions for informatics research (Japan) | `gated`: apply per dataset under the IDR terms | Data List | Read each dataset page first |
| GSK (Gengo Shigen Kyokai) | https://www.gsk.or.jp/en/ (200) | Japanese speech data, lexicons, corpora, terminology | Per-resource application form by e-mail; price = handling fee + postage (sometimes royalties); members get one free item a year | Catalogue page | Return or destroy after use; Japanese-language procedure |

### 15. Computer vision and general machine-learning benchmarks
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| UCI Machine Learning Repository | https://archive.ics.uci.edu/ (200) | Databases, domain theories and data generators for ML | Download; licence per dataset UNVERIFIED | Search; `ucimlrepo` Python package | Some entries only link to external hosts |
| OpenML | https://www.openml.org/ (200) | ML datasets, tasks, runs and benchmarks | `open` | REST API (answered); Python and R libraries | None noted |
| Kaggle Datasets | https://www.kaggle.com/datasets (200) | User-uploaded datasets and competition data | CLI and API need Kaggle credentials; web download rules UNVERIFIED | Search; Kaggle CLI | User mirrors may not carry the original terms |
| TensorFlow Datasets catalog | https://www.tensorflow.org/datasets/catalog/overview (200) | Catalogue of dataset loaders | The library fetches from the original sources; some need a manual download | Catalogue; Python library | A loader is not a licence; check the source |
| Registry of Open Data on AWS | https://registry.opendata.aws/ (200) | Datasets available through AWS resources | Mostly `open`; some need registration (re3data) | Search; GitHub-based registry | Maintained by third parties, not AWS |

### 16. Chemistry and materials science
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| PubChem | https://pubchem.ncbi.nlm.nih.gov/ (200; pages showed a browser check to scripts) | Chemical substances, compounds and bioassays deposited by many sources | `open` | PUG-REST API (answered anonymously); FTP (re3data) | Use the API, not page scraping |
| NOMAD | https://nomad-lab.eu/ (200) | Computational and experimental materials data from many codes | `open` and free; uploads can be access-controlled | Search GUI; API (info endpoint answered) | None noted |
| Materials Cloud Archive | https://archive.materialscloud.org/ (200) | Computational materials science records | `open` per re3data; own page UNVERIFIED | REST API (answered); OAI-PMH (re3data) | None noted |
| Materials Data Facility | https://www.materialsdatafacility.org/ (200) | Materials science datasets published through Globus | Discovery open; publishing needs a free Globus account | Search; API UNVERIFIED | Large transfers go through Globus |
| CCDC Access Structures | https://www.ccdc.cam.ac.uk/structures/ (200) | Deposited crystal structures (CCDC with FIZ Karlsruhe) | Free to view and retrieve single structures; advanced search needs a database licence | Structure search | Bulk use needs a licence |

### 17. Physics and astronomy
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| CERN Open Data Portal | https://opendata.cern.ch/ (200) | Collider event and simulated data, software, documentation | `open` under open licences with DOIs; released after experiment embargo periods | Search; REST API (answered) | Only released subsets |
| HEPData | https://www.hepdata.net/ (200; JSON search answered 403 behind a bot check) | Data tables from particle-physics publications | `open` access | Search page | Scripted queries challenged today |
| MAST (STScI) | https://archive.stsci.edu/ (200) | Space-telescope archives and high-level science products | Public data downloadable; embargoed data exist (re3data) | Portal search; API https://mast.stsci.edu/api/v0/invoke (500 "missing parameter": endpoint exists) | New data may be proprietary |
| HEASARC (NASA) | https://heasarc.gsfc.nasa.gov/ (200) | High-energy astrophysics catalogues and mission archives | `open` | Catalogue search; download scripts, wget, curl | None noted |
| ESO Science Archive | https://archive.eso.org/cms.html (200) | Raw and processed data from ESO telescopes | Public after the proprietary period (normally one year); registration per re3data | Raw-data query form; Science Portal | Recent data proprietary |
| CDS Strasbourg | https://cds.unistra.fr/ (200) | Astronomical catalogue service and object database | `open` | Web services, also through listed mirrors | Security incident on 2026-11-11: some services offline; mirrors listed |

### 18. Education
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| NCES (US) | https://nces.ed.gov/ (200) | US education statistics and survey data | Public data and tools; restricted-use files need an IES restricted-use data licence | Data tools | Licensee obligations for restricted use |
| UNESCO UIS Data Browser | https://databrowser.uis.unesco.org/ (200) | International education indicators | `open`: view, filter, download csv, excel or json | Data browser; API https://api.uis.unesco.org/api/public/versions (answered) | Indicators, not microdata |
| IEA Data Repository | https://www.iea.nl/data-tools/repository (200) | Data from international large-scale education assessments | Download after accepting the Disclaimer and License Agreement | Repository page; IDB Analyzer | Analysis needs the IDB Analyzer tool |
| LearnSphere DataShop (CMU) | https://pslcdatashop.web.cmu.edu/ (200) | Learning-interaction data from educational technology | Login (InCommon or Google). Some datasets open to any logged-in user, others need the PI's permission (`gated`) | Search; web services (re3data: REST) | Per-dataset permission |
| Explore education statistics (England) | https://explore-education-statistics.service.gov.uk/ (200) | England education statistics releases | `open` download | Search; API documented | England only |

### 19. General-purpose and institutional repositories, and cross-repository search engines
| Repository | URL | Holds | Typical access | Search/API | Caution |
|---|---|---|---|---|---|
| Google Dataset Search | https://datasetsearch.research.google.com/ (200) | Search engine over dataset metadata on the web | Links out to the host | Search UI; no API stated | Verify every hit on its host |
| re3data | https://www.re3data.org/ (200) | Registry of research data repositories | `open` metadata (CC0) | Search; open API (used for this map) | Lists repositories, not datasets |
| Harvard Dataverse | https://dataverse.harvard.edu/ (202 bot challenge; https://dataverse.harvard.edu/api/info/version answered) | General-purpose research data | Mostly `open`; some files restricted, with terms of use or a guestbook | Search; native REST API; OAI-PMH, SWORD (re3data) | Restricted files need an access request |
| Figshare | https://figshare.com/ (202/403, blocked); API https://api.figshare.com/v2/articles (answered) | General-purpose research outputs | UNVERIFIED (re3data: open, embargoed) | REST API | Own pages blocked to scripts |
| Dryad | https://datadryad.org/ (200) | Curated research data | `open`: all data under CC0; depositors pay a data publishing charge unless sponsored | Search; REST API (answered) | No personally identifiable data accepted |
| data.gov (US) | https://data.gov/ (200) | *Catalogue* of US government open data | `open`; links to agency hosts | Search; API UNVERIFIED (CKAN endpoint returned 404) | Data live on agency sites |
| data.europa.eu | https://data.europa.eu/en (200) | *Catalogue* of EU and national open data portals | Mostly `open` | Search; search API (answered); SPARQL (re3data) | Also has a European Register for Protected Data |
