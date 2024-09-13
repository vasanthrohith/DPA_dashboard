import pandas as pd
from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import time
import os
from dotenv import load_dotenv
import requests


load_dotenv()
# GitHub access token (replace with your token)
token = os.getenv("github_token")



class Analyse_repo:
    def __init__(self, repo_name):

        try:
            
            g = Github(token)
            repo = g.get_repo(repo_name)

            # Fetch commits, pull requests, and issues
            self.commits = repo.get_commits()
            self.pull_requests = repo.get_pulls(state='all')
            self.issues = repo.get_issues(state='all')
            print("Total commits count > ",self.commits.totalCount)

        except Exception as error:
            print(error)

    def Give_analytics(self, limit_count=5000):
         self.limit_count=limit_count
         return self.get_commit_data()

    def get_commit_data(self,):
        """Commit Metrics: Commit frequency per developer and code churn (lines added/deleted)"""
        self.commit_data = []
        self.count = 0
        
        
        for commit in self.commits:
            try:
            
                print("commit > ", self.count)
                if self.count == self.limit_count:
                    self.count=0
                    break
                author = commit.commit.author.name
                commit_date = commit.commit.author.date  # Get the commit date

                if author:
                    self.commit_data.append({
                        "Author": author,
                        "Commits": 1,  # 1 commit per row
                        "Code Churn": commit.stats.total,
                        "Date": commit_date  # Store the commit date
                    })

                self.count += 1


            except RateLimitExceededException as e:
                        print(e.status)
                        print('Rate limit exceeded')
                        time.sleep(300)
                        continue
            except BadCredentialsException as e:
                print(e.status)
                print('Bad credentials exception')
                break
            except UnknownObjectException as e:
                print(e.status)
                print('Unknown object exception')
                break
            except GithubException as e:
                print(e.status)
                print('General exception')
                break
            except requests.exceptions.ConnectionError as e:
                print('Retries limit exceeded')
                print(str(e))
                time.sleep(10)
                continue
            except requests.exceptions.Timeout as e:
                print(str(e))
                print('Time out exception')
                time.sleep(10)
                continue
        try:

            # Convert commit_data list to DataFrame
            commit_df = pd.DataFrame(self.commit_data)
            commit_df['Date'] = pd.to_datetime(commit_df['Date']).dt.date  # Convert to date format
            commit_df.to_csv('commits.csv', index=False)
            print("CSV created successfully... commits_data")

            self.get_pr_data()

            

        except Exception as error:
            print("Error in -get_commit_data-",error)

    def get_pr_data(self,):
        """Pull Request Metrics: Number of PRs opened, merge rate, PR size, review time"""
        print("--get_pr_data--")
        self.pr_data = {}
        for pr in self.pull_requests:
            try:
                print("Pull Request Metrics>",self.count)
                if self.count==self.limit_count:
                    self.count=0
                    break
                author = pr.user.login

                if author:
                    self.pr_data.setdefault(author, {"prs": 0, "merged": 0, "total_pr_size": 0, "total_review_time": 0})
                    self.pr_data[author]["prs"] += 1
                    if pr.merged:
                        self.pr_data[author]["merged"] += 1
                    self.pr_data[author]["total_pr_size"] += pr.additions + pr.deletions
                    if pr.merged:
                        self.pr_data[author]["total_review_time"] += ((pr.merged_at - pr.created_at).seconds)/3600
                self.count+=1

            except RateLimitExceededException as e:
                        print(e.status)
                        print('Rate limit exceeded')
                        time.sleep(300)
                        continue
            except BadCredentialsException as e:
                print(e.status)
                print('Bad credentials exception')
                break
            except UnknownObjectException as e:
                print(e.status)
                print('Unknown object exception')
                break
            except GithubException as e:
                print(e.status)
                print('General exception')
                break
            except requests.exceptions.ConnectionError as e:
                print('Retries limit exceeded')
                print(str(e))
                time.sleep(10)
                continue
            except requests.exceptions.Timeout as e:
                print(str(e))
                print('Time out exception')
                time.sleep(10)
                continue

        try:

            # Convert pr_data dictionary to DataFrame
            pr_df = pd.DataFrame.from_dict(self.pr_data, orient='index')
            pr_df.reset_index(inplace=True)
            pr_df.columns = ['Author', 'PRs', 'Merged PRs', 'Total PR Size', 'Total Review Time (hours)']

            pr_df.to_csv('pr_data.csv', index=False)
            print("csv created successfully... pr_data")

            return self.get_issue_data()


        except Exception as error:
            print("Error in -get_pr_data-",error)
            return False

    def get_issue_data(self,):
        """Issue Metrics: Number of issues resolved, average time to resolve"""
        print("--get_issue_data--")
        self.issue_data = {}
        
        for issue in self.issues:
            print("issue >", self.count)

            try: 
                if self.count == self.limit_count:
                    self.count = 0
                    break
                if issue.closed_at and issue.assignee:
                    assignee = issue.assignee.login
                    closed_at = issue.closed_at.date()  # Get the issue closed date
                    self.issue_data.setdefault(assignee, {"resolved_issues": 0, "total_resolution_time": 0, "dates": []})
                    self.issue_data[assignee]["resolved_issues"] += 1
                    self.issue_data[assignee]["total_resolution_time"] += (issue.closed_at - issue.created_at).seconds / 3600
                    self.issue_data[assignee]["dates"].append(closed_at)  # Store the date when the issue was closed

                self.count += 1

            except RateLimitExceededException as e:
                        print(e.status)
                        print('Rate limit exceeded')
                        time.sleep(300)
                        continue
            except BadCredentialsException as e:
                print(e.status)
                print('Bad credentials exception')
                break
            except UnknownObjectException as e:
                print(e.status)
                print('Unknown object exception')
                break
            except GithubException as e:
                print(e.status)
                print('General exception')
                break
            except requests.exceptions.ConnectionError as e:
                print('Retries limit exceeded')
                print(str(e))
                time.sleep(10)
                continue
            except requests.exceptions.Timeout as e:
                print(str(e))
                print('Time out exception')
                time.sleep(10)
                continue

        try:
            print(self.issue_data)

            # Convert issue_data dictionary to DataFrame
            issue_df = pd.DataFrame.from_dict(self.issue_data, orient='index')
            issue_df.reset_index(inplace=True)
            issue_df.columns = ['Assignee', 'Resolved Issues', 'Total Resolution Time (hours)', 'Dates']
            issue_df['Avg Issue Resolution Time (hours)'] = issue_df['Total Resolution Time (hours)'] / issue_df['Resolved Issues']

            # Explode the dates list into individual rows for each closure date
            issue_df = issue_df.explode('Dates')

            # Rename the 'Dates' column to 'Date' for compatibility with the visualization
            issue_df['Date'] = issue_df['Dates']
            issue_df.drop('Dates', axis=1, inplace=True)

            # Save to CSV
            issue_df.to_csv('issue_data.csv', index=False)
            print("CSV created successfully... issue_data")

            return self.calc_developer_performance()

        except Exception as error:
             print("Error in -get_issue_data-", error)
             return False

    def calc_developer_performance(self,):
        """Combine data into a single list"""
        print("--calc_developer_performance--")
        self.data = []
        for author in set(self.commit_data.keys()).union(self.pr_data.keys()).union(self.issue_data.keys()):

            row = {
                "Developer": author,
                "Commits": self.commit_data.get(author, {}).get("commits", 0),
                "Code Churn (Lines)": self.commit_data.get(author, {}).get("code_churn", 0),
                "PRs Opened": self.pr_data.get(author, {}).get("prs", 0),
                "PRs Merged": self.pr_data.get(author, {}).get("merged", 0),
                "Avg PR Size": self.pr_data.get(author, {}).get("total_pr_size", 0) / max(self.pr_data.get(author, {}).get("prs", 1), 1),
                "Avg PR Review Time (Days)": self.pr_data.get(author, {}).get("total_review_time", 0) / max(self.pr_data.get(author, {}).get("merged", 1), 1),
                "Issues Resolved": self.issue_data.get(author, {}).get("resolved_issues", 0),
                "Avg Issue Resolution Time (hours)": self.issue_data.get(author, {}).get("total_resolution_time", 0) / max(self.issue_data.get(author, {}).get("resolved_issues", 1), 1)
            }
            self.data.append(row)

            count+=1

        # Create a DataFrame
        df = pd.DataFrame(self.data)

        # Save to CSV
        df.to_csv('developer_performance.csv', index=False)

        print("CSV file 'developer_performance.csv' created successfully!")

        return True


# obj=Analyse_repo(repo_name="scikit-learn/scikit-learn")
# print(obj.Give_analytics(limit_count=5))      

