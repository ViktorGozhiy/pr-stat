# pr-stat overview
Script for generating a pull request statistics table

```commandline
+--------------------------------------------------------------------------------------------------------------------------------------------------+
|                                            Pull Request Statistics for repo-user/repo-name                                                       |
+-------------------+---------+------+------------------+----------+---------+-----------------------------+---------------------------------------+
| User              | Created | Open | Required Reviews | Reviewed | Ignored | Average Review Time (hours) | Average Time To Close Own PRs (hours) |
+-------------------+---------+------+------------------+----------+---------+-----------------------------+---------------------------------------+
| Samuel Jackson    | 0       | 0    | 6                | 3        | 2       | 8.25                        | 0                                     |
| Olivia Rodriguez  | 1       | 0    | 5                | 0        | 4       | 0                           | 16.17                                 |
| William Thompson  | 0       | 0    | 5                | 1        | 3       | 15.49                       | 0                                     |
| Ava Martinez      | 2       | 1    | 4                | 2        | 2       | 11.96                       | 10.3                                  |
| James Wilson      | 3       | 0    | 2                | 1        | 0       | 6.26                        | 13.78                                 |
| Sophia Davis      | 0       | 0    | 0                | 0        | 0       | 0                           | 0                                     |
| Michael Garcia    | 0       | 0    | 0                | 0        | 0       | 0                           | 0                                     |
+-------------------+---------+------+------------------+----------+---------+-----------------------------+---------------------------------------+
```

# Run
 * Add dependencies: `pip install -r requirements.txt`
 * Edit script and add your values: `OWNER`, `REPO`, `ACCESS_TOKEN`, `START_DATE`
 * Run with command: `python main.py`
