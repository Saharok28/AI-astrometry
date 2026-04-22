import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileWriterTool, DirectoryReadTool, FileReadTool
from github import Github

load_dotenv()

OR_KEY = os.getenv("OPENROUTER_API_KEY")

dev_llm = LLM(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    api_key=OR_KEY
)

# Architect & QA Model (Fast and efficient)
fast_llm = LLM(
    model="openrouter/google/gemini-2.0-flash-001",
    api_key=OR_KEY
)


def upload_to_github(repo_name, folder):
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not token:
        return "Error: GitHub token missing."
    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(repo_name)
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                if os.path.isfile(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        repo.create_file(file, "Initial commit", f.read())
        return f"Done: https://github.com/{user.login}/{repo_name}"
    except Exception as e:
        return f"GitHub Error: {str(e)}"


# --- AGENTS ---
architect = Agent(
    role='Architect',
    goal='Design file structure and logic for {topic}',
    backstory='Senior Software Architect. Provides clear file maps.',
    llm=fast_llm,
    verbose=True
)

developer = Agent(
    role='Developer',
    goal='Write clean code and save files to {folder}',
    backstory='Senior Fullstack Engineer. Professional at writing robust code.',
    llm=dev_llm,
    verbose=True
)

qa = Agent(
    role='QA Engineer',
    goal='Verify code quality. Output "APPROVED" if everything is correct.',
    backstory='Detailed oriented tester. Checks for bugs and errors.',
    llm=fast_llm,
    verbose=True
)

if __name__ == "__main__":
    while True:
        print("\n--- AI AGENT SYSTEM ---")
        topic = input("Task (or 'exit'): ")
        if topic.lower() in ['exit', 'quit']: break

        print("Output Location:\n1. Default (./projects)\n2. Custom path")
        choice = input("Select (1/2): ")

        base_path = input("Enter full path: ").strip() if choice == '2' else "./projects"
        repo_name = input("Project name: ")
        final_path = os.path.join(base_path, repo_name)

        if not os.path.exists(final_path):
            os.makedirs(final_path, exist_ok=True)

        # Tools initialization for specific folder
        writer = FileWriterTool()
        d_reader = DirectoryReadTool(directory=final_path)
        f_reader = FileReadTool()

        developer.tools = [writer, d_reader, f_reader]
        qa.tools = [d_reader, f_reader]

        # Tasks Definition
        t1 = Task(
            description=f"Create a technical plan for: {topic}",
            expected_output="Detailed list of files and their functions.",
            agent=architect
        )
        t2 = Task(
            description=f"Write code based on the plan and save it to {final_path}",
            expected_output="All project files created on disk.",
            agent=developer,
            context=[t1]
        )
        t3 = Task(
            description=f"Review files in {final_path}. Verify they work. Write APPROVED if done.",
            expected_output="Final audit report with APPROVED status.",
            agent=qa,
            context=[t2]
        )

        crew = Crew(agents=[architect, developer, qa], tasks=[t1, t2, t3], verbose=True)

        print("\nStarting AI Crew...")
        try:
            result = str(crew.kickoff(inputs={'topic': topic, 'folder': final_path}))

            if "APPROVED" in result.upper():
                print(f"\n[!] Success. Project saved to: {os.path.abspath(final_path)}")
                if input("Push to GitHub? (y/n): ").lower() == 'y':
                    print(upload_to_github(repo_name, final_path))
            else:
                print("\n[?] QA did not approve the project. Check output for details.")
        except Exception as e:
            print(f"\n[X] Error during execution: {e}")