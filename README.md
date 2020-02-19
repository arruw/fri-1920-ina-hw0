# Introduction to Network Analysis - Homework #0

## 1. Network software

## 2. Network collection

```sql
SELECT mh.id, from_visit, url
FROM moz_historyvisits mh 
INNER JOIN moz_places mp ON mp.id = mh.place_id
ORDER BY mh.id 
```


## 3. Network analysis