from Project import *
from GPT import *

class Generator(Project):
    def __init__(self, cwd='./projects'):
        self.cwd = cwd
        self.gpt = GPT()
        super().__init__(cwd)

    def open(self, id):
        self.openProject(f"{self.cwd}/{id}")
    
    def generate(self, id, idea, content_type="paper"):
        self.open(id)
        if "content" not in self.project or self.project["type"] != content_type:
            self.project["type"] = content_type
        
        if "subject" not in self.project:
            self.ideaToSubject(idea)
        
        if self.project["type"] == "thesis":
            if "thesis" not in self.project:
                self.subjectToThesis(self.project["subject"])
            if "thesis_review" not in self.project:
                self.thesisReview(self.project["thesis"])
            if "repo" not in self.project:
                self.thesisToCode(self.project["thesis_review"])
        if self.project["type"] == "paper":
            if "paper" not in self.project:
                self.subjectToPaper(self.project["subject"])
            if "paper_final" not in self.project:
                self.paperReview(self.project["paper"])
            if "repo" not in self.project:
                self.paperToCode(self.project["paper_final"])
            if "saved" not in self.project:
                self.generateGithubRepo()
    
    def ideaToSubject(self, idea):
        print("Converting the idea into a research subject...")
        prompt = self.gpt.getPrompt("prompts/idea-to-subject.txt", {
            "idea": idea
        })
        response = self.gpt.ask(prompt, "", model="o3-mini")
        self.project["idea"] = idea
        self.project["subject"] = response
        self.saveProject()
    
    def subjectToThesis(self, subject):
        print("Writing the first draft of the PhD Thesis...")
        prompt = self.gpt.getPrompt("prompts/subject-to-thesis.txt", {
            "thesis_subject": json.dumps(subject),
            "author": "(Generate a name)"
        })
        response = self.gpt.ask(prompt, "", model="o3-mini")
        self.project["thesis"] = response["content"]
        self.saveProject()
        self.write(f"{self.projectPath}/thesis-draft.md", self.project["thesis"])
    
    def subjectToPaper(self, subject):
        print("Writing the first draft of the Research Paper...")
        prompt = self.gpt.getPrompt("prompts/subject-to-paper.txt", {
            "research_subject": json.dumps(subject),
            "author": "(Generate a name)"
        })
        response = self.gpt.ask(prompt, "", model="o3-mini")
        self.project["paper"] = response["content"]
        self.saveProject()
        self.write(f"{self.projectPath}/paper-draft.md", self.project["paper"])
    
    def thesisReview(self, thesis):
        print("Writing the finale version of the PhD Thesis...")
        prompt = self.gpt.getPrompt("prompts/thesis-review.txt")

        response = self.gpt.ask(thesis, prompt, model="o3-mini")
        self.project["thesis_review"] = response["final_draft"]
        self.saveProject()
        self.write(f"{self.projectPath}/thesis-final.md", self.project["thesis_review"])
    
    def paperReview(self, thesis):
        print("Writing the finale version of the Research Paper...")
        prompt = self.gpt.getPrompt("prompts/paper-review.txt")

        response = self.gpt.ask(thesis, prompt, model="o3-mini")
        self.project["paper_final"] = response["final_draft"]
        self.saveProject()
        self.write(f"{self.projectPath}/paper-final.md", self.project["paper_final"])
    
    def thesisToCode(self, thesis, instructions=""):
        print("Writing the code...")
        prompt = self.gpt.getPrompt("prompts/thesis-to-code.txt", {
            "thesis": thesis,
            "instructions": instructions
        })
        response = self.gpt.ask(prompt, "", model="o3-mini")
        self.project["repo"] = response
        self.saveProject()

    def paperToCode(self, thesis, instructions="1 tab = 4 spaces, DRY code, cleanly organized in classes. Include a requirement.txt"):
        print("Writing the code for the paper...")
        prompt = self.gpt.getPrompt("prompts/paper-to-code.txt", {
            "instructions": instructions
        })
        response = self.gpt.ask(prompt, thesis, model="o3-mini")
        self.project["repo"] = response
        self.saveProject()
    
    def generateGithubRepo(self):
        repo = self.project["repo"]["github-repo-name"]
        for file in self.project["repo"]["files"]:
            filename = file["filename"]
            self.write(f"{self.projectPath}/{repo}/{filename}", file["content"])
        self.project["saved"] = True
        self.saveProject()
        

gen = Generator()
# gen.generate("test", "Leveraging Attention Mechanisms in Deep Learning Architectures for Accurate Stock Market Direction Prediction: A Multi-Source Financial Time Series Analysis")
# gen.generate("diff-sat-paper", "Spatio-Temporal Diffusion Models for Satellite Imagery: Enhancing Environmental Monitoring and Land-Use Change Detection")
gen.generate("diff-timeserie-anomaly", "Anomaly Detection in Time-Series Data via Diffusion Models")
