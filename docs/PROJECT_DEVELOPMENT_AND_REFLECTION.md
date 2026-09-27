\# Project Development Process and Personal Reflection



The Problem and My Initial Perspective



The main goal of this project was to build an application capable of analysing EU-funded research projects and, based primarily on their descriptions and objectives, identifying the Sustainable Development Goal targets that best match the problems they are trying to address.



I found this problem particularly interesting because CORDIS contains a very large amount of information distributed across thousands of research projects. Although this information is publicly available, understanding the broader contribution of these projects in a structured way is far from straightforward. Automating part of this process can therefore help address an information-management and administrative challenge by making the project landscape easier to explore, compare and interpret.



The beginning of the project was relatively familiar to me. Exploring the raw data, understanding its structure and interpreting the patterns that emerged felt natural because of my previous experience with data analysis and my interest in statistics. At that stage, the work was close to the type of analytical process I already enjoyed: inspecting a dataset, understanding its variables, identifying useful information and gradually forming a clearer picture of the problem before attempting to build a solution.



Moving Beyond Data Analysis



The first genuinely difficult stage came when the project moved from traditional data analysis into machine learning, artificial intelligence and application development.



As an Economics student whose practical experience had mainly been in data analysis, I did not initially have significant exposure to the more technical aspects of machine learning, model evaluation, software development and deployment. Many of the concepts and methods involved were new to me.



At the same time, machine learning, AI and statistics are subjects that strongly interest me, so I decided to treat the project not only as a competition entry but also as an opportunity to learn.



With the assistance of tools such as ChatGPT and Codex, I was able to work through unfamiliar concepts, understand the logic behind different components of the system, debug problems and gradually build the application. These tools became important development and learning resources, but the process still required me to understand what was being built, examine the outputs, identify problems and make decisions about how the project should evolve.



Understanding the code itself was one of the most difficult parts. I did not want to simply execute scripts without knowing what they were doing. I wanted to understand why each major component existed, what problem it was solving and how changing it could affect the final results. This took considerably more time than I initially expected.



From General SDG Relevance to Exact Target Contribution



One of the most important conceptual lessons came when I realised that identifying broad SDG relevance was not enough.



A research project can clearly relate to a goal such as SDG 9 without necessarily contributing to a specific target within that goal. The actual task was therefore more difficult than assigning projects to general themes. The system had to determine whether the activities and objectives described by a project meaningfully supported the wording and intent of an exact SDG target.



This also made the distinction between STRONG, WEAK and UNSUPPORTED contributions much more difficult.



A project may contain words such as sustainability, innovation, resilience, technology or research, but the presence of related terminology does not automatically justify a mapping. The important question is whether the project is actually performing, supporting or substantially advancing the action described by the target.



This was also where the limitations of a simple similarity-based approach became clear.



A semantic retrieval model can be very useful for identifying potentially relevant targets, but similarity alone cannot determine whether the relationship represents genuine contribution. A project and a target may sound similar while describing significantly different objectives.



For this reason, the final architecture separated the problem into two stages. The retrieval component first narrowed the 169 SDG targets down to a smaller set of candidates. A second semantic verification stage then examined those candidates more carefully and determined whether the available evidence justified accepting the mapping.



This eventually led to a more conservative system. I preferred allowing a project to remain unmapped rather than forcing it into an SDG target that could not be properly justified.



That decision became an important principle of the final application: more mappings are not necessarily better mappings.



Development, Validation and Learning from Failure



The development process was highly iterative.



The semantic verifier went through several versions, and every iteration revealed different weaknesses. Some versions became better at distinguishing supported from unsupported mappings but performed poorly when separating strong and weak contributions. Other approaches became too conservative or produced associations that appeared reasonable at first but did not survive closer examination.



There were many occasions when a new version initially appeared promising, only for validation to show that another part of the system had deteriorated.



This was one of the most frustrating but also one of the most educational parts of the project. There were moments during the month of development when I genuinely considered abandoning the work because solving one problem seemed to create another.



To evaluate the system more objectively, I created a human-reviewed development benchmark rather than relying entirely on the outputs of the model itself. Two independent reviewers assessed project-target pairs, with part of the sample reviewed by both. The fact that the reviewers did not always agree was itself informative: exact SDG-target contribution can sometimes involve genuine ambiguity even for humans.



The benchmark was then used to compare successive verifier versions.



One of the most important lessons I learned from this process was that improving one metric does not automatically mean that the overall model has improved. Precision, recall, class imbalance, false positives and false negatives all tell different parts of the story.



The final verifier, V8, was not selected because it produced perfect results. In fact, it did not pass every internal performance threshold that I had defined during development. It performed well in some areas while remaining weaker in others.



Rather than hiding those weaknesses, I decided to document them.



This changed the way I thought about model evaluation. Before this project, I tended to think about machine-learning performance mainly through headline metrics such as accuracy. During development, I learned how easily a single number can provide an incomplete impression of a system.



I also learned why repeatedly evaluating and modifying a model against the same development benchmark can gradually weaken the meaning of that benchmark.



For that reason, the verifier was eventually frozen rather than endlessly modified in pursuit of better-looking development metrics.



The final production results are therefore not presented as perfect ground truth. They are presented as evidence-backed model mappings with clearly documented limitations.



Building the Final Product



Once the retrieval and verification architecture had been frozen, the focus changed from experimentation to creating a complete product.



I did not want the final result to remain only as a notebook containing model outputs. I wanted to create something that another user or evaluator could explore without needing to understand every technical decision or run the entire modelling pipeline.



The final controlled demonstration sample contains 150 CORDIS projects.



For each project, the retrieval stage selected the ten most relevant candidates from the 169 SDG targets, producing 1,500 project-target candidate pairs. These candidates were then evaluated by the semantic verification pipeline.



The final output contains 231 supported mappings, covering 100 of the 150 projects. The remaining 50 projects were left unmapped because the system did not identify a sufficiently supported target assignment.



I consider those unmapped projects an important part of the result rather than a failure. The system was not designed to guarantee that every research project receives an SDG classification.



Each accepted mapping contains more than a project identifier and an SDG label. The final dataset also includes the exact target, a categorical confidence level, whether the contribution is classified as DIRECT or INDIRECT, supporting evidence from the project information and an explanation for the mapping.



The result is therefore not simply a classification table. It is an explainable dataset in which individual mappings can be inspected and questioned.



The outputs were then converted into several formats. CSV and Excel files allow further analysis, while the notebook documents the methodology, evaluation approach, quality-control process and main findings.



The final stage was the creation of the public Streamlit application.



The application allows users to search individual projects, inspect their mapped SDG targets, review the supporting evidence and explanation, filter results according to SDG, confidence and contribution type, explore aggregate distributions and download the underlying data.



Importantly, the public application performs no live language-model inference. It presents the frozen and audited results of the final pipeline.



For me, this was the stage that transformed the work from a modelling experiment into a small end-to-end data product.



Limitations and Future Work



The project was developed under three main constraints: limited computing hardware, limited previous technical experience in machine learning and AI, and a relatively small budget.



As a university student, these constraints were expected. I did not have access to high-end computing infrastructure or large-scale cloud resources, and I could not experiment extensively with every architecture or model that might have been relevant to the problem.



My academic background also influenced the process. I approached the project primarily from Economics and Data Analysis rather than from Computer Science or formal Machine Learning training.



As a result, a significant amount of development time was simultaneously learning time.



These constraints also limited the scale of the final experiment. With greater resources, I would have liked to test a wider range of embedding and language models, process a much larger part of the CORDIS collection and construct a larger independently human-labelled evaluation dataset.



For this reason, the final 150-project dataset should be understood as a controlled demonstration of the methodology, not as an exhaustive analysis of the entire CORDIS database.



Nevertheless, I believe I used the available resources as effectively as I reasonably could. My objective was not to create the most computationally expensive system possible, but to develop a complete, explainable and reproducible pipeline within realistic constraints.



The final result is not intended to represent a perfect or definitive solution. It represents what I was able to build after approximately one month of development using the hardware, knowledge, budget and time available to me, and it is a result I am personally very satisfied with.



In future work, I would like to work with larger European public datasets, particularly data made available through European data portals, and explore other problems that could benefit from the combination of data analysis, machine learning and application development.



I would also like to participate in similar challenges and build larger projects as my technical knowledge develops.



Rather than viewing this application as the end of this type of work, I see it as the beginning.



Personal Experience and Final Reflection



After approximately one month of working on this project, I learned far more than I originally expected.



The most important outcome for me was not only developing a better understanding of machine learning, artificial intelligence and statistical modelling. I also experienced the complete process of building a data-driven application from the ground up: starting with raw data, designing the pipeline, validating outputs, debugging problems, creating reproducible results, developing an interface and finally deploying a public application.



Coming from an Economics background, many parts of that process initially felt outside my technical comfort zone.



I struggled to understand some of the methods and ideas of a field that I had never formally studied in depth. I struggled with the code and with understanding exactly what different components were doing.



But eventually, I did understand them.



By the end of the project, I was able to follow and reason about a system that would have seemed significantly beyond my technical level when I started.



AI tools played an important role in making this possible. ChatGPT and Codex helped me understand unfamiliar concepts, debug problems, learn how different components could be built and gradually move from an idea to a working application.



For me, the most valuable lesson was learning how to use AI as a tool for building while still understanding, checking and questioning the work being produced.



Without this kind of assistance, completing a project of this technical scope within the competition deadline would have been extremely difficult.



At the same time, the project also taught me that using AI effectively is very different from simply asking it to generate an answer.



Many of the most important decisions still required judgment: defining what a valid mapping meant, recognising misleading outputs, deciding how validation should work, interpreting metrics, determining when further iteration was no longer justified and deciding how honestly to communicate the limitations of the final system.



The project therefore became an exercise not only in using AI, but also in learning how to supervise, evaluate and integrate AI-assisted work into a coherent technical process.



Most importantly, this experience strengthened my interest in machine learning, AI, data science and statistics.



Building an application from an initial dataset all the way to a publicly accessible product made these fields feel considerably more accessible than they did before I started.



What initially appeared to be a highly technical area outside my academic background gradually became something I could understand, work with and continue learning.



For that reason, I see this project as more than a competition submission.



It could represent an important first step toward the academic and professional direction I want to pursue, including the possibility of completing a postgraduate degree abroad in Data Science, Business Analytics, Machine Learning or a related field.



Regardless of the final competition result, the project gave me practical experience, greater technical confidence and a much clearer understanding of the type of work I would like to continue exploring.



For me, that is probably the most valuable result of the entire project.

