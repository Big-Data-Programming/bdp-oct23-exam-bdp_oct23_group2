### GitHub Data:

1. **User Information:**

   - GitHub Username - maybe
   - Full Name - yes
   - Email -yes

2. **Repository Information:**

   - Repository Name
   - Language   -yes
   - Number of Stars -yes
   - Number of Forks
   - Last Commit Date - maybe

3. **Contributions:**

   - Total Commits 
   - Commit History (timestamps, messages)

4. **Issues and Pull Requests:**
   - Number of Open Issues
   - Number of Closed Issues   - yes
   - Number of Open Pull Requests -yes
   - Number of Merged Pull Requests  -yes
   - Projects/project descriptions (README files) - yes

#### Database Columns:

**User Table:**

- `id` (Primary Key)
- `github_username` (Unique) -
- `full_name`
- `email`

**Repository Table:**

- `id` (Primary Key)
- `user_id` (Foreign Key referencing User)
- `name`
- `language`
- `stars`
- `forks`
- `last_commit_date`

**Commit Table:**

- `id` (Primary Key)
- `repository_id` (Foreign Key referencing Repository)
- `timestamp`
- `message`

**Issue Table:**

- `id` (Primary Key)
- `repository_id` (Foreign Key referencing Repository)
- `open_issues`
- `closed_issues`

**Pull Request Table:**

- `id` (Primary Key)
- `repository_id` (Foreign Key referencing Repository)
- `open_prs`
- `merged_prs`

**GitHub User Contribution Table:**

- `id` (Primary Key)
- `user_id` (Foreign Key referencing GitHub User)
- `total_commits`
- `total_pr_opened`
- `total_pr_merged`
- `total_issues_opened`
- `total_issues_closed`
- `daily_date`
- `daily_commits`
- `daily_pr_opened`
- `daily_pr_merged`
- `daily_issues_opened`
- `daily_issues_closed`

### Stack Overflow Data:

#### Columns to Fetch:

1. **User Information:**

   - Stack Overflow Username
   - Reputation -  yes
   - Badges -yes

2. **Question and Answer History:**

   - Total Questions Asked
   - Total Answers Provided -yes
   - Upvotes and Downvotes on Questions
   - Upvotes and Downvotes on Answers -yes

3. **Tags and Topics:**
   - Tags associated with the user's questions and answers -maybe

#### Database Columns (Example):

**StackOverflowUser Table:**

- `id` (Primary Key)
- `stackoverflow_username` (Unique)
- `reputation`
- `badges`

**QuestionAnswer Table:**

- `id` (Primary Key)
- `user_id` (Foreign Key referencing StackOverflowUser)
- `total_questions`
- `total_answers`
- `question_upvotes`
- `question_downvotes`
- `answer_upvotes`
- `answer_downvotes`

**Tags Table:**

- `id` (Primary Key)
- `user_id` (Foreign Key referencing StackOverflowUser)
- `tag_name`
