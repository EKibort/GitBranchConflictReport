# Detection merge conflicts between branches of same git repository

Example:
```
python git_branch_conflicts.py "D:\Reps\gitconflictstest" "conflicts.html"
```

Report looks like:

<table class="tg">
<tr><th>branch</th><th>branch</th><th>files</th></tr>
<tr><td>b1</td><td>b2</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
<tr><td rowspan="3">b2</td><td>b1</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
<tr><td>master</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
<tr><td>b3</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
<tr><td>b3</td><td>b2</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
<tr><td>master</td><td>b2</td><td><ul>
<li>folder/f1.txt</li>
<li>test.txt</li>
</ul></td></tr>
</table>

Output example:

```
2017-09-17 20:59:19,508 INFO Starting for 'D:\Reps\gitconflictstest'
2017-09-17 20:59:19,535 INFO Fetching branches ....
2017-09-17 20:59:19,685 INFO Checkout 'b1'
2017-09-17 20:59:20,040 INFO    Merging with 'master'
2017-09-17 20:59:20,438 INFO            Detect conflicts in files:
2017-09-17 20:59:20,440 INFO                    'CHANGELOG' - ignored
2017-09-17 20:59:20,440 INFO    Merging with 'b3'
2017-09-17 20:59:20,872 INFO            Detect conflicts in files:
2017-09-17 20:59:20,873 INFO                    'CHANGELOG' - ignored
2017-09-17 20:59:20,873 INFO    Merging with 'b2'
2017-09-17 20:59:21,240 INFO            Detect conflicts in files:
2017-09-17 20:59:21,241 INFO                    'test.txt'
2017-09-17 20:59:21,241 INFO                    'folder/f1.txt'
2017-09-17 20:59:21,242 INFO Checkout 'b2'
2017-09-17 20:59:21,617 INFO    Merging with 'master'
2017-09-17 20:59:22,020 INFO            Detect conflicts in files:
2017-09-17 20:59:22,021 INFO                    'test.txt'
2017-09-17 20:59:22,021 INFO                    'folder/f1.txt'
2017-09-17 20:59:22,021 INFO    Merging with 'b3'
2017-09-17 20:59:22,357 INFO            Detect conflicts in files:
2017-09-17 20:59:22,363 INFO                    'test.txt'
2017-09-17 20:59:22,364 INFO                    'folder/f1.txt'
2017-09-17 20:59:22,364 INFO Checkout 'b3'
2017-09-17 20:59:22,778 INFO    Merging with 'master'
2017-09-17 20:59:23,151 INFO Checkout 'master'
```
