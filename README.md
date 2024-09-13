<h1>Developer Performance Dashboard</h1>

<h2>Overview</h2>

<p>This project provides a Streamlit-based dashboard that delivers insights into developer performance using data from an open-source GitHub repository. It enables users such as project managers, team leads, and developers to view key metrics related to commits, pull requests, issues, and code reviews.</p>

<p>The dashboard includes a <strong>natural language interface</strong>, powered by a Large Language Model (LLM), that allows users to query developer performance metrics using conversational language.</p>

<h2>Features</h2>

<h3>1. Data Collection</h3>
<ul>
  <li>Integrated with GitHub API to fetch repository data.</li>
  <li>Collected data includes:
    <ul>
      <li>Commits</li>
      <li>Pull Requests (PRs)</li>
      <li>Issues</li>
      <li>Code Reviews</li>
    </ul>
  </li>
</ul>

<h3>2. Metrics Calculations</h3>
<ul>
  <li><strong>Commit Metrics</strong>: Frequency per developer, code churn (lines added/deleted).</li>
  <li><strong>PR Metrics</strong>: Number of PRs, merge rate, average size, and review time.</li>
  <li><strong>Issue Metrics</strong>: Number of resolved issues, average resolution time.</li>
  <li><strong>Code Review Metrics</strong>: Number of reviews, review depth (comments per review).</li>
  <li><strong>Cycle Time Metrics</strong>: Time from issue creation to PR creation and time from PR creation to merge.</li>
</ul>

<h3>3. Dashboard Components</h3>
<ul>
  <li><strong>Overview Page</strong>: Summary of key metrics and performance trends over time.</li>
  <li><strong>Individual Developer Page</strong>: Detailed metrics for each developer, with comparisons to team averages.</li>
  <li><strong>PR Analysis Page</strong>: PR size distribution and life cycle analysis.</li>
  <li><strong>Issue Tracking Page</strong>: Trends in issue resolution and backlog analysis.</li>
  <li><strong>Code Review Insights Page</strong>: Review participation and thoroughness analysis.</li>
</ul>

<h3>4. Natural Language Querying with LLM</h3>
<ul>
  <li>Query developer performance metrics using a text input field.</li>
  <li>Integrated with an LLM (e.g., GPT-3.5 or GPT-4-o mini) to handle natural language queries.</li>
  <li>Example queries include:
    <ul>
      <li>"Who has been the most productive developer in the last month?"</li>
      <li>"What's the average PR review time for [Developer Name]?"</li>
      <li>"Show me the trend of bug fix efficiency over the past quarter."</li>
    </ul>
  </li>
</ul>

<h2>Technology Stack</h2>
<ul>
  <li><strong>Frontend</strong>: Streamlit</li>
  <li><strong>GitHub API Integration</strong>: PyGithub</li>
  <li><strong>Data Manipulation</strong>: Pandas</li>
  <li><strong>Visualizations</strong>: Plotly</li>
  <li><strong>LLM Integration</strong>: OpenAI API</li>
</ul>

<h2>Installation</h2>

<ol>
  <li><strong>Clone the Repository:</strong>
    <pre><code>git clone https://github.com/vasanthrohith/DPA_dashboard.git
cd DPA_dashboard
</code></pre>
  </li>

  
<li><strong>Install Dependencies:</strong>
    <p>Ensure you have Python 3.8+ installed. Then run:</p>
    <pre><code>pip install poetry
poetry install
</code></pre>
</li>

<li><strong>Set Up .env:</strong>
    <p>Create a <code>.env</code> file in the root directory and add your GitHub API token:</p>
    <pre><code>github_token=your_github_token
openai_api_key=your_openai_api_key
</code></pre>
</li>

  <li><strong>Run the Application:</strong>
    <p>Launch the Streamlit dashboard by running:</p>
    <pre><code>streamlit run dashboard.py</code></pre>
  </li>
</ol>

<h2>Usage</h2>

<ol>
  <li><strong>Input GitHub Repository URL:</strong>
    <p>On the first page of the dashboard, enter the URL of the repository you want to analyze.</p>
  </li>

  <li><strong>View Metrics:</strong>
    <p>Once the data is fetched, explore the various pages for metrics on commits, PRs, issues, and code reviews.</p>
  </li>

  <li><strong>Natural Language Querying:</strong>
    <p>Use the "Ask a Question" section to interact with the LLM by typing queries related to developer performance.</p>
  </li>
</ol>

<h2>Data Storage</h2>

<ul>
  <li>Data is stored as CSV files during the POC phase.</li>
  <li>Daily data fetching and storage are implemented to keep the metrics updated.</li>
</ul>

<h2>Future Enhancements</h2>

<ul>
  <li>Expand to support multiple repositories.</li>
  <li>Add more detailed code review metrics.</li>
</ul>

