select
    "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."prices",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."preview"
from "shopapp_product"
where not "shopapp_product"."archived"
order by "shopapp_product"."name" asc, "shopapp_product"."prices" asc;


SELECT
"shopapp_product"."id",
"shopapp_product"."name",
"shopapp_product"."description",
 "shopapp_product"."prices",
 "shopapp_product"."discount",
 "shopapp_product"."created_at",
 "shopapp_product"."archived",
 "shopapp_product"."preview"
 FROM "shopapp_product"
 WHERE "shopapp_product"."id" = 2 LIMIT 21; args=(2,); alias=default


SELECT
"shopapp_productimage"."id",
"shopapp_productimage"."product_id",
"shopapp_productimage"."image",
"shopapp_productimage"."description"
FROM "shopapp_productimage"
WHERE "shopapp_productimage"."product_id" IN (2); args=(2,); alias=default
