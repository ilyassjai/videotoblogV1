# Backend Documentation

# 🗂️ Core Application

## Overview

The core application converts YouTube lecture videos into structured blog articles. It extracts slide images, transcribes video content, and generates articles in Markdown format.

## Functionality

- **Input:** Accepts a YouTube video link as a command-line argument.
- **Processing:** Extracts slides and transcribes video content using AI models.
- **Content Generation:** Combines transcribed text and slide images into a Markdown article.
- **Integration:** Uploads slide images to Google Cloud Storage and stores article metadata in Firestore.
- **Cleanup:** Deletes temporary files after article generation.

## Usage

- **Input:** Requires a YouTube video link as a command-line argument.
- **Output:** Provides a JSON response with a message indicating processing completion and the article ID.

## Environment Variables

- `OPENAI_KEY`: API key for OpenAI GPT-3 model.
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to Google Cloud credentials file.
# 🗂️ Flask Application

The Flask application serves as the API endpoint for interacting with the backend.

### Endpoint: /process-youtube-link (POST)

Endpoint to receive YouTube video conversion requests from the client.

#### Method: POST
- Body Parameters:
  - `youtubeLink` (str): YouTube video link to be processed.
- Returns:
  - JSON object: `{ "taskId": "<task_id>" }`, where `task_id` is the ID of the Celery task for asynchronous processing.

### Endpoint: /simple_start_task (GET)

Endpoint to manually start a simple Celery task.

#### Method: GET
- Returns:
  - Task ID of the started Celery task.

### Endpoint: /simple_task_status/<task_id> (GET)

Endpoint to check the status of a Celery task.

#### Method: GET
- Path Parameter:
  - `task_id` (str): ID of the Celery task.
- Returns:
  - Status of the Celery task.

### Endpoint: /simple_task_result/<task_id> (GET)

Endpoint to retrieve the result of a completed Celery task.

#### Method: GET
- Path Parameter:
  - `task_id` (str): ID of the Celery task.
- Returns:
  - JSON object: `{ "result": <task_result> }`, where `task_result` is the result of the Celery task.

### Endpoint: /all_tasks_status (GET)

Endpoint to get the status of all registered Celery tasks.

#### Method: GET
- Returns:
  - JSON object containing information about all registered Celery tasks.

# 🗂️ Celery Tasks

## Long Running Task (task for testing)

### Function: longtime_add

A Celery task that simulates a long-running process by sleeping for 10 seconds.

#### Arguments:
- `x` (int): First integer operand.
- `y` (int): Second integer operand.

#### Returns:
- `int`: The product of `x` and `y`.

## YouTube Video Processing Task

### Function: youtube_link_process

A Celery task that processes a YouTube video link to convert it into a blog article.

#### Arguments:
- `youtube_link` (str): YouTube video link to be processed.

#### Returns:
- `dict` or `str`: Dictionary containing the processed output if successful, or an error message if the subprocess fails or the output file cannot be read.

## 🖥️ Docker Instructions

To start the dockerized app:
1. Make sure your Docker daemon is running.
2. Open terminal and navigate to the root directory.
3. Type: `docker-compose up --build`
   This will build and start the Docker containers.
4. To stop the containers, type: `docker-compose down`

To start apps separately:
- Navigate to the directory of the part you want to run separately:
  - `cd flask_app` or `cd core_app`
- Create and activate a virtual environment:
  1. Install virtualenv package if not already installed:
     - On Windows: `python -m pip install virtualenv`
     - On macOS/Linux: `pip3 install virtualenv`
  2. Create a new virtual environment:
     - On Windows: `python -m venv my_venv`
     - On macOS/Linux: `python3 -m venv my_venv`
  3. Activate the virtual environment:
     - On Windows: `my_venv\Scripts\activate`
     - On macOS/Linux: `source my_venv/bin/activate`
- Install required libraries from requirements.txt:
  - `pip install -r requirements.txt`
- Start the application:
  - For flask_app, run: `python src/app.py`
  - For core_app, run: `python src/main.py`


# 📝 Example of a Blog Post:
## Presentation Summary

In this presentation, Fran Sharf from Data Chefs discusses Enterprise Intelligence applications in the Private Equity and Investment Banking industry. The talk focuses on a consulting engagement with Data Chefs, highlighting the integration of Enterprise Intelligence tools in the financial sector.

## Outline

- **Private Equity and Enterprise Intelligence**
- **Email Alerts**
- **Leads for Private Equity Investment Bankers**
- **Private Social Network (LinkedIn for the bank)**
- **Integration of the Knowledge Graph in the wider Enterprise Data Ecosystem**

This summary provides an overview of the key topics covered in the presentation, emphasizing the importance of Enterprise Intelligence in the private equity and investment banking sectors.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_1.png))

# Private Equity and Investment Banking in Enterprise Intelligence

In the context of private equity and investment banking, there is a focus on enterprise intelligence. This involves developing applications such as email alert systems, investment banker tools, and private enterprise social networks. These applications are built alongside a knowledge graph that expands as more data sources are integrated.

## Development of Applications

Three key applications have been developed:
1. **Email Alert Application**
2. **Leits Application for Investment Bankers**
3. **Private Enterprise Social Network**

## Knowledge Graph Expansion

The knowledge graph has been a central focus, expanding in size and integrating with the enterprise information system. This dual effort of building and integrating the knowledge graph has been crucial in enhancing the overall enterprise ecosystem.

## About the Data Chefs

The Data Chefs are a boutique consultancy based in New York City, specializing in enterprise data management. With expertise in semantic technologies, knowledge graphs, and data management, they offer a range of services including technology development, mentorship, proofs of concepts, and machine learning.

## Conclusion

The Data Chefs are experts in their field, with a strong focus on leveraging data to drive insights and innovation in various sectors including finance, legal, and technology. Their dedication to advancing enterprise intelligence through knowledge graphs and advanced applications sets them apart in the industry.

![Image]([slidemse\slide_2.png](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_2.png))

## Investment Banking Overview

In the context of private equity, investment banking operates on a global scale. The client in focus is a sizable bank with thousands of bankers spread across offices on five continents. These bankers specialize in regions, industries, or sectors, sometimes with overlapping expertise. Their primary role involves tracking companies for financing purposes.

### Role of Investment Banking

Investment banking serves companies by providing financial services such as lending money, facilitating acquisitions, and offering investment advice. It blends a social component of being present at the right time for deals with a number-crunching aspect that requires proficiency in financial analysis tools like Excel.

### Focus on Companies

In the banking domain, companies are the central entities that investment bankers engage with. Understanding the financial needs and opportunities of these companies is crucial for successful financial transactions.

In summary, investment banking plays a vital role in the financial ecosystem by connecting companies with the necessary capital and expertise to support their growth and strategic initiatives.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_3.png)

## Private Equity Overview

In the world of private equity, the focus is on dealing with privately held companies, contrasting with public companies that are listed on stock exchanges. When a company is public, it can issue more stock to raise funds, whereas private companies need to seek financing from banks or investors.

## Role of Investment Bankers

Investment bankers play a crucial role in private equity transactions. They assess the viability of projects, negotiate financing deals, and earn a percentage of the transaction as their fee.

## Acquisition and Sale of Companies

Private equity also involves companies acquiring or selling other businesses. Investment bankers facilitate these transactions, which can range from large acquisitions to smaller startups being bought by industry giants like Google.

## Skills Required

Success in private equity requires a blend of social skills and financial acumen. Building relationships, identifying potential deals, and crunching numbers are all part of the job.

## The Vision: Connecting The Firm’s Data Ecosystem

The long-term goal is to establish an enterprise knowledge graph that integrates with major applications like Salesforce. This graph will sit atop the firm's data infrastructure, enhancing data management and decision-making processes.

## MDM Integration

Master Data Management (MDM) plays a key role in integrating various data sources and applications within the firm's ecosystem.

---

By following these guidelines, the text has been transformed into a concise and structured Markdown format suitable for a blog post.

![Image]((https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_4.png))

# Transforming Transcribed Text into Markdown for a Blog

In the midst of building an Enterprise data Lake, a company sought to enhance their processes through the incorporation of knowledge graphs. With a plethora of data sources including internal data, purchased data via APIs, and data generated and consumed by various software systems, they had initiated efforts around data quality, governance, and Master Data Management (MDM).

## Methodology: Where to Start?

1. **Start small and scale**
2. **Begin with an end user application as the first project**
3. **Expand the knowledge graph and domain**
4. **Demonstrate rapid integration ease with each additional step leveraging the knowledge graph**

After achieving initial successes, the company can aim for more ambitious projects.

By following these steps, the company was able to infuse added value into their data processes and accelerate their journey towards a more robust and efficient data ecosystem.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_5.png)

## Knowledge Graph Project Strategy

When embarking on a Knowledge Graph project within an Enterprise, it is crucial to start small and demonstrate value quickly. The initial focus should be on developing an end-user application that utilizes the Knowledge Graph. By proving the usefulness of the application, you can then gradually expand the Knowledge Graph and its domain.

### Starting Small

Begin with a small end-user application to showcase the capabilities of the Knowledge Graph. This approach allows for rapid validation of the project's viability and sets the foundation for future expansions.

### Scaling Up

As success is achieved with the initial application, gradually expand the Knowledge Graph and incorporate additional data sources. This iterative process not only demonstrates the scalability of the project but also reduces the cost of developing new applications.

### Project Progression

After establishing a solid foundation with smaller applications, aim for more ambitious projects that leverage the matured Knowledge Graph. One such example is an email alert system designed for investment bankers to track company news and engage with executives effectively.

### Implementation Details

The project involved integrating banker interests, company news, and internal databases into the Knowledge Graph. By developing a comprehensive ontology to represent entities such as companies, persons, and events, the system efficiently facilitated the alerting process.

By following a progressive and iterative approach, organizations can effectively harness the power of Knowledge Graphs to enhance decision-making and drive innovation in their operations.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_6.png)

# Transforming Transcribed Text into Markdown Format for a Blog

## Introduction
In this blog post, we delve into the intricacies of a project that involved creating a social network within the banking sector. The project aimed to enhance connectivity and information sharing among bankers by leveraging advanced data integration and analysis techniques.

## Project Overview
The core objective of the project was to develop a social network that would allow bankers to efficiently discover and connect with relevant companies and executives based on specific criteria. This network utilized a Knowledge Graph that integrated various data sources, including internal databases and vendor-provided information.

## Enhancements and Features
- **Data Integration**: The social graph incorporated existing data sources from previous applications while also adding new sources to enhance its scope.
- **Scale and Performance**: Significant enhancements were made to ensure the network could handle a large volume of data and user interactions effectively.
- **Mobile and Desktop Applications**: Two distinct applications were developed, catering to both mobile and desktop users for seamless accessibility.
- **Connectivity Features**: Users could inquire about contacting specific individuals, executives at particular companies, or obtaining contact lists based on predefined criteria.

## Evolution of Criteria and Functionality
The project evolved from assisting bankers in identifying relevant companies based on specific criteria to enabling automated alerts based on user-defined parameters. This progression facilitated proactive engagement with companies and executives aligned with the bankers' interests and preferences.

## Integration of Social Networking Features
To further enhance connectivity and streamline communication, an Enterprise social network was developed on top of the existing platform. This expansion required scaling the Knowledge Graph significantly and incorporating additional data sources to support a broader network of relationships.

## Conclusion
The development of this social network within the banking sector marked a significant advancement in fostering collaboration and information sharing among industry professionals. By leveraging advanced data integration techniques and innovative networking functionalities, the project aimed to revolutionize how bankers interact and engage with companies and executives within their domain.

By following these guidelines and structuring the content accordingly, we have successfully transformed the transcribed text into a concise and informative Markdown format suitable for a blog post.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_7.png)

# Integrating Knowledge Graphs in Enterprise Information Systems

In the realm of Knowledge Graph (KG) projects, sustainability hinges on seamless integration within the overarching enterprise information system. This integration is achieved through several key strategies:

## Data Lake Integration

The knowledge graph is strategically positioned atop the data lake, facilitating efficient data management and accessibility.

## Data Quality Assurance

Ensuring the integrity of KG data, rigorous data quality checks are conducted, with feedback loop mechanisms in place to address any discrepancies.

## Data Governance Alignment

Harmonizing ontology and taxonomy terms with Data Governance software guarantees that KG mappings align seamlessly with metadata fields.

## Master Data Management (MDM) Collaboration

The knowledge graph generates unique identifiers for resources, fostering a bidirectional flow of information with MDM software to maintain data consistency.

## Leveraging Data Science Capabilities

Exporting the KG to Databricks Graph Frames empowers the creation of predictive analytics models, unlocking valuable insights for informed decision-making.

By adhering to these integration practices, organizations can optimize the utility and effectiveness of their Knowledge Graph initiatives within the broader enterprise context.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_8.png)

## The Data Chefs: Transforming Enterprise Data Ecosystem

In the realm of enterprise data management, the Data Chefs have emerged as the guiding force, orchestrating a symphony of data processes to enhance the organization's data ecosystem.

### Data Transformation and Governance

The Data Chefs embarked on a journey to refine the enterprise ecosystem, where the knowledge graph took center stage atop the data lake. They meticulously curated high-quality data, conducting thorough quality analyses and liaising with the data quality team to ensure data integrity.

### Integration with Data Governance and Master Data Management

Seamless integration with data governance software facilitated the alignment of terms, concepts, and properties in ontologies with the data sources. This meticulous mapping to the knowledge graph ensured adherence to data governance policies. Moreover, in the realm of Master Data Management (MDM), the Data Chefs played a pivotal role in data integration within the knowledge graph, fostering the maintenance of essential data lists within MDM software.

### Empowering Data Science Teams

The Data Chefs paved the way for data science teams to seamlessly access and leverage data through various access points, including APIs and integration with data bricks. This empowered the teams to harness the power of graph data for modeling and training, leveraging tools like Prot for ontology and Pool Party for taxonomy.

### Scalability and Computational Prowess

The Data Chefs demonstrated their prowess by constructing a vast industry taxonomy and scaling the graph to handle several billion triples on a cluster of AllegroGraph DBs. Their computational acumen ensured efficient processing, minimizing the need for repetitive Sparkle queries within The Social Network.

### Conclusion

The Data Chefs' transformative efforts encompassed the development of three data-intensive applications, the construction of a substantial graph, ontology, and taxonomy, all seamlessly integrated into the enterprise data ecosystem. Their expertise, honed across diverse application domains, stands as a testament to their commitment to data excellence.

For further inquiries and to experience the transformative power of the Data Chefs, visit [Ine VAIAL](#).

---

By aligning the text with the guidelines provided, the summary has been enhanced to offer a more concise and structured overview of the Data Chefs' impact on the enterprise data ecosystem.

![Image](https://github.com/ilyassjai/videotoblogV1/blob/main/slidemse/slide_9.png)
