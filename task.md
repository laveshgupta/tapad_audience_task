An *audience* is defined by a set of string values.

Audiences are stored on a file system using the following partitioning scheme:
```
/var/data/audiences/{year}/{month}/{day}/{audience-id}/part-00000.txt
```

In the above example, `{year}` would be the full four digits of the year, `{month}` would be the two digit numerical value for the month of the year, and `{day}` would be the two digit numerical value for the day of the month.

The `{audience-id}` is the numerical identifier which identifies the audience for a given file path.

Each of these partitioned directories can have many files, e.g.:
```
/var/data/audiences/2017/12/01/789/part-00000.txt
/var/data/audiences/2017/12/01/789/part-00001.txt
...
/var/data/audiences/2017/12/01/789/part-01024.txt
```

The file resources addressed by the above paths would contain a string value per each line. This string value would represent a single audience member.

All values found within the file resource could be described as audience member *additions* for that given day.

Keep in mind that `/var/data/audiences` is an example path. When designing your solution, you need not place data in this specific directory. Any directory will do (e.g. `/tmp/my-solution/audiences`).

Audiences could both grow and shrink over time, and as such, have a similar way of expressing audience member *removals* for a given day.

Audience removal operations for a given audience for a given day are stored on the file system using the following scheme:
```
/var/data/audiences/{year}/{month}/{day}/-{audience-id}/part-00000.txt
```

Everything is exactly the same as the additions described above, save for the negative sign that prefixes the `{audience-id}`.

Some audiences will have a small number of operations on a given day, others will have a large number of operations. Your solution should be prepared to handle millions of audience operations for a given day.

Audiences are bought by our clients, and a given client will specify which audience, by identifier, they are interested in, along with their expiration requirements.

Clients receive these audience datasets on a daily basis.

If a client specifies an expiration time of 15 days for a given audience, we would deliver them our view of said audience using the audience data that we have collected from the last 15 days.