Select * From recipes
where id in
	(SELECT tbl1.recipes_id FROM
		(SELECT a.recipes_id, count(*)
		FROM recipes_ingredients A
		WHERE a.ingredients_id in
			(SELECT id
			from ingrediants 
			where  name = 'cheese' or name = 'tortilla' or name = 'pasta'
			)
		GROUP BY a.recipes_id) tbl1
		join(
			Select mylist.recipes_id, c from
				(SELECT a.recipes_id, count(*) c
				FROM recipes_ingredients A
				GROUP BY a.recipes_id) 
				as mylist) 
	 		tbl2
		on tbl1.recipes_id = tbl2.recipes_id
		and tbl1.count = tbl2.c)



