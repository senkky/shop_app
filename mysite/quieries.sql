select "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."archived", "shopapp_product"."preview" from "shopapp_prod
uct" where "shopapp_product"."id" = 2 limit 21;
select "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."description" from "shopapp_productimage" where "shopapp_productimage"."product_id" in (2); args=(2,); alias=default
