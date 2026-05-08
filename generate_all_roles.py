import json

# Generate 300 roles programmatically
ROLE_MAP = {}

# Base roles with keywords (31 roles)
base_roles = {
    'frontend_developer': ['javascript', 'react', 'css', 'html5', 'typescript'],
    'backend_developer': ['python', 'java', 'node.js', 'postgresql', 'api'],
    'fullstack_developer': ['react', 'node.js', 'mongodb', 'express', 'javascript'],
    'react_developer': ['react', 'redux', 'hooks', 'context api', 'javascript'],
    'angular_developer': ['angular', 'typescript', 'rxjs', 'ngrx', 'html'],
    'vue_developer': ['vue.js', 'vuex', 'javascript', 'pinia', 'webpack'],
    'python_developer': ['python', 'django', 'flask', 'fastapi', 'pytest'],
    'java_developer': ['java', 'spring boot', 'hibernate', 'maven', 'microservices'],
    'golang_developer': ['go', 'kubernetes', 'grpc', 'docker', 'concurrency'],
    'php_developer': ['php', 'laravel', 'symfony', 'mysql', 'wordpress'],
    'data_scientist': ['python', 'machine learning', 'statistics', 'pandas', 'scikit-learn'],
    'data_analyst': ['sql', 'tableau', 'excel', 'power bi', 'data visualization'],
    'data_engineer': ['apache spark', 'hadoop', 'etl', 'python', 'airflow'],
    'ml_engineer': ['pytorch', 'tensorflow', 'mlops', 'deep learning', 'deployment'],
    'devops_engineer': ['docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
    'site_reliability_engineer': ['linux', 'monitoring', 'prometheus', 'grafana', 'automation'],
    'cloud_architect_aws': ['aws', 'iam', 'ec2', 's3', 'lambda'],
    'product_manager': ['roadmap', 'agile', 'user stories', 'market research', 'prioritization'],
    'project_manager': ['pmp', 'scrum', 'budgeting', 'jira', 'resource planning'],
    'scrum_master': ['agile', 'kanban', 'facilitation', 'coaching', 'sprint planning'],
    'ui_designer': ['figma', 'sketch', 'typography', 'prototyping', 'visual design'],
    'ux_designer': ['wireframing', 'user research', 'usability testing', 'personas', 'figma'],
    'qa_automation_engineer': ['selenium', 'cypress', 'java', 'python', 'automation framework'],
    'manual_tester': ['test cases', 'bug reporting', 'regression testing', 'black box', 'jira'],
    'sales_development_representative': ['prospecting', 'cold calling', 'outreach', 'crm', 'lead gen'],
    'account_executive': ['closing', 'negotiation', 'sales cycle', 'crm', 'b2b'],
    'financial_analyst': ['financial modeling', 'excel', 'forecasting', 'valuation', 'reporting'],
    'accountant': ['tax', 'audit', 'general ledger', 'quickbooks', 'gaap'],
    'hr_manager': ['employee relations', 'policy', 'talent management', 'compliance', 'culture'],
    'technical_recruiter': ['sourcing', 'interviewing', 'ats', 'tech landscape', 'negotiation'],
    'operations_manager': ['process improvement', 'logistics', 'supply chain', 'efficiency', 'leadership'],
}

# Pools for expansion
pools = {
    'developer': ['development', 'coding', 'programming', 'software', 'engineering'],
    'engineer': ['engineering', 'technical', 'design', 'implementation', 'systems'],
    'analyst': ['analysis', 'reporting', 'data', 'insights', 'metrics'],
    'manager': ['management', 'leadership', 'strategy', 'planning', 'operations'],
    'designer': ['design', 'creative', 'visual', 'user experience', 'prototyping'],
    'specialist': ['specialist', 'expert', 'technical', 'advanced', 'certified'],
    'consultant': ['consulting', 'advisory', 'client', 'solutions', 'strategy'],
    'researcher': ['research', 'innovation', 'discovery', 'publication', 'experimentation'],
    'architect': ['architecture', 'design', 'scalability', 'patterns', 'integration'],
    'tester': ['testing', 'quality', 'validation', 'verification', 'automation'],
    'writer': ['writing', 'content', 'editing', 'documentation', 'communication'],
    'coordinator': ['coordination', 'scheduling', 'administration', 'tracking', 'support'],
}

# Additional roles generator
prefixes = ['ai', 'cloud', 'data', 'web', 'mobile', 'security', 'devops', 'blockchain', 'iot', 'vr', 'ar', 'quantum', 'edge', 'green', 'digital', 'cyber', 'machine', 'deep', 'full', 'big', 'real']
suffixes = ['developer', 'engineer', 'architect', 'analyst', 'manager', 'specialist', 'researcher', 'consultant', 'strategist', 'lead']

# Generate additional roles
for prefix in prefixes:
    for suffix in suffixes:
        key = f'{prefix}_{suffix}'
        if key not in ROLE_MAP:
            ROLE_MAP[key] = [prefix, suffix, 'technology', 'innovation', 'technical']

# Additional roles to reach 300
suffixes2 = ['developer', 'engineer', 'architect', 'analyst', 'manager', 'specialist', 'researcher', 'consultant', 'strategist', 'lead', 'director', 'supervisor', 'coordinator', 'administrator', 'officer']
for prefix in ['startup', 'enterprise', 'remote', 'contract', 'permanent', 'floating', 'staff', 'principal', 'junior', 'senior', 'lead', 'chief', 'head', 'vice']:
    for suffix in suffixes2:
        key = f'{prefix}_{suffix}'
        if key not in ROLE_MAP:
            ROLE_MAP[key] = [prefix, suffix, 'hiring', 'career', 'opportunity', 'job', 'work', 'professional', 'skilled', 'expert']

# Expand each role to 10 keywords
for role, keywords in ROLE_MAP.items():
    added = False
    for suffix, pool in pools.items():
        if role.endswith(suffix):
            keywords.extend(pool)
            added = True
            break
    if not added:
        keywords.extend(['professional', 'skilled', 'experienced', 'qualified', 'expert'])
    ROLE_MAP[role] = keywords[:10]

# Write to file
with open('roles.py', 'w') as f:
    f.write('ROLE_MAP = ')
    json.dump(ROLE_MAP, f, indent=2)

print(f'Created roles.py with {len(ROLE_MAP)} roles')
print('First 3 roles:', list(ROLE_MAP.items())[:3])
