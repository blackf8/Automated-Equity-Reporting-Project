# Automated-Equity-Research-Project-AER-

Currently calcWACC is working, but only under TSLA. 

pandas optimization needed for WACC
FCFF will be halted until pandas can operate


Who We Are
We are a group of Brandeis & Colgate Business and Computer Science students who are
looking to incorporate our mixed interests together in a project. We are looking to create a
software that uses financial models to predict stocks. We have a wide range of expertise, with
each of us having different levels of experience. Brendon and Allen have the most experience in
finance, having taken multiple courses as well as being involved in investment club and Tamid
fund. However, we all have some experience with stocks and Rohit has taken a few financial
classes. We all have experience with computer science, with Rohit, Tuan, and Prabu having
essentially completed the computer science major. Rohit, Tuan, and Prabu also have experience
in machine learning, and neural networks.
Synopsis
Our project is a software that accepts a company ticker as input and uses DCF modeling
and recently released financial statements, such as quarterly reports, to provide a valuation.
The software will subsequently output a valuation summary for the company. At a baseline, we
are planning on implementing methods using data provided by Yahoo!Finance using a related
API. As we develop our software, we hope to improve the accuracy of our calculations by
implementing more advanced processes, such as different valuation models, a capital structure
comparator, a technical analysis component to determine buy/sell prices, etc; these processes
may require data we cannot acquire ourselves, and consequently may require assistance to
access.
Purposes
● Getting started with investing, learning through practice
● Acquiring practical experience connecting our business & computer science classroom
learnings
● To provide helpful software to Brandeis affiliates such as: Clubs, Students, Professors
Procedure
Step 1: Create a back testing framework
The first step in our program is to create a testing framework that allows us to test
different investment strategy modules. The framework will look at past financial data
through different APIs such as Yahoo finance, use the module to determine which stocks
are optimal, and compare this with future financial data to determine how successful
the module is. Initially we will likely use a very simple module such as one day trading
just as a starting point
Step 2: Implement the DCF model and improve with testing framework
Initially, we will implement a DCF valuation model and use that to observe and predict
stocks. However, using our back testing framework we will be able to make changes to

the valuation model and observe the success rate. We hope to make improvements that
will increase the success rate of the modules.
Step 3: Creating the final program and formatting output reports
Most of step 1 is creating a testing framework that we can use to enhance our predictive
algorithm. After we find the optimal strategy, we need to implement it into a real-time
program. By looking at current financial data rather than past one, the program will use
our module to advise on optimal stocks to invest in. Ideally, it will also provide a small
report that shows the key financials and the reasoning for the decisions in a concise
manner. We will likely over the course of the next semester/school year test this
program in real time and see how it compares to market trends.

Program Layout
Parts:
● Input
○ Api calls
○ Gathers user input
○ Data cleaning
○ Data processing
● Box 1 Volume [PROTOTYPE]
○ Contains Volume logic
○ Evaluates tickets
○ Compares ticker evaluations
○ Purely meant as a placeholder
● Box 2 DCF
○ Contains DCF logic
○ Evaluates tickers
○ Compares ticker evaluations
● Box 3,4,5,... [to be implemented later; each box represents a different valuation method]
○ Research done over time to determine best boxes
○ Will be implemented in later weeks
● Output
○ Compares evaluations
○ Visualizes results
○ Compares to reality
○ Flask Dashboard / Frontend Implementations
● Pipe
○ Holds the various module objects
○ Manages data throughout the pipeline

We will later create a variation of the code that utilizes a specific set of boxes and rather than
comparing to reality, simply uses current data to make future predictions.

Scheduling and Project Management
In order to manage our group and keep track of everyone’s progress, we will be using Trello to
organize everyone's tasks. Below, you can see a screenshot of our Trello board currently which
shows the work we will be completing over the first 2 weeks of our project. As time goes on, we
will update the trello with more activities and tasks which can be seen in the Timeline Category
below.
