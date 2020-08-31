--[Joburg_Fresh_produce_commodity_raw]
ALTER TABLE [Joburg_Fresh_produce_commodity_raw]
DROP COLUMN IF EXISTS YTD_total_value_sold,
	 COLUMN IF EXISTS MTD_total_value_sold,
	 COLUMN IF EXISTS YTD_total_qty_sold,
	 COLUMN IF EXISTS MTD_total_qty_sold,
	 COLUMN IF EXISTS YTD_total_kg_sold,
	 COLUMN IF EXISTS MTD_total_kg_sold;

ALTER TABLE [Joburg_Fresh_produce_commodity_raw]
ADD YTD_total_value_sold NUMERIC(20,2),
	MTD_total_value_sold NUMERIC(20,2),
	YTD_total_qty_sold NUMERIC(10),
	MTD_total_qty_sold NUMERIC(10),
	YTD_total_kg_sold NUMERIC(10),
	MTD_total_kg_sold NUMERIC(10)

UPDATE [Joburg_Fresh_produce_commodity_raw]
set YTD_total_kg_sold = REPLACE(SUBSTRING([total_kg_sold],1,CHARINDEX('M', [total_kg_sold])-1),',',''),
	 MTD_total_kg_sold = REPLACE(SUBSTRING([total_kg_sold],CHARINDEX(':', [total_kg_sold])+2,20),',',''),
	YTD_total_value_sold = REPLACE(SUBSTRING([total_value_sold],2,CHARINDEX('M', [total_value_sold])-2),',',''),
	 MTD_total_value_sold = REPLACE(SUBSTRING([total_value_sold],CHARINDEX(':', [total_value_sold])+3,20),',',''),
	 YTD_total_qty_sold = REPLACE(SUBSTRING([total_qty_sold],1,CHARINDEX('M', [total_qty_sold])-1),',',''),
	 MTD_total_qty_sold = REPLACE(SUBSTRING([total_qty_sold],CHARINDEX(':', [total_qty_sold])+2,20),',','')

--[Joburg_Fresh_produce_container_raw]
ALTER TABLE [Joburg_Fresh_produce_container_raw]
DROP COLUMN IF EXISTS YTD_value_sold,
	 COLUMN IF EXISTS MTD_value_sold,
	 COLUMN IF EXISTS YTD_qty_sold,
	 COLUMN IF EXISTS MTD_qty_sold,
	 COLUMN IF EXISTS YTD_kg_sold,
	 COLUMN IF EXISTS MTD_kg_sold,
	 COLUMN IF EXISTS Ave_price_kg;

ALTER TABLE [Joburg_Fresh_produce_container_raw]
ADD YTD_value_sold NUMERIC(20,2),
	MTD_value_sold NUMERIC(20,2),
	YTD_qty_sold NUMERIC(10),
	MTD_qty_sold NUMERIC(10),
	YTD_kg_sold NUMERIC(10),
	MTD_kg_sold NUMERIC(10),
	Ave_price_kg NUMERIC(10,2)

UPDATE [Joburg_Fresh_produce_container_raw]
set YTD_value_sold = REPLACE(SUBSTRING([value_sold],2,CHARINDEX('M', [value_sold])-2),',',''),
	MTD_value_sold = REPLACE(SUBSTRING([value_sold],CHARINDEX(':', [value_sold])+3,20),',',''),
	YTD_qty_sold = REPLACE(SUBSTRING([qty_sold],1,CHARINDEX('M', [qty_sold])-1),',',''),
	MTD_qty_sold = REPLACE(SUBSTRING([qty_sold],CHARINDEX(':', [qty_sold])+2,20),',',''),
	YTD_kg_sold = REPLACE(SUBSTRING([kg_sold],1,CHARINDEX('M', [kg_sold])-1),',',''),
	MTD_kg_sold = REPLACE(SUBSTRING([kg_sold],CHARINDEX(':', [kg_sold])+2,20),',',''),
	Ave_price_kg = replace(average_price_per_kg,'R','')

--product combination

ALTER TABLE [Joburg_Fresh_produce_product_combination_raw]
DROP COLUMN IF EXISTS total_value_sold2,
	 COLUMN IF EXISTS total_kg_sold2,
	 COLUMN IF EXISTS average2,
	 COLUMN IF EXISTS highest_price2,
	 COLUMN IF EXISTS Ave_price_kg2,
	 COLUMN IF EXISTS highest_price_per_kg2;

ALTER TABLE [Joburg_Fresh_produce_product_combination_raw]
ADD total_value_sold2 NUMERIC(10,2),
	total_kg_sold2 NUMERIC(10,2),
	average2 NUMERIC(10,2),
	highest_price2 NUMERIC(10,2),
	Ave_price_kg2 NUMERIC(10,2),
	highest_price_per_kg2 NUMERIC(10,2)

UPDATE [Joburg_Fresh_produce_product_combination_raw]
set total_value_sold2 = replace(replace([total_value_sold],'R',''),',',''),
	total_kg_sold2 =replace(replace([total_kg_sold],',','.'),',',''),
	average2 = replace(replace([average],'R',''),',',''),
	highest_price2 = replace(replace([highest_price],'R',''),',',''),
	Ave_price_kg2 = replace(replace([ave_per_kg],'R',''),',',''),
	highest_price_per_kg2 = replace(replace([highest_price_per_kg],'R',''),',','')

ALTER TABLE [Joburg_Fresh_produce_product_combination_raw]
ALTER COLUMN [total_qty_sold] NUMERIC(15,2)


--PickNPay_woolwothrs_shoprite
--rerun only once
ALTER TABLE [PickNPay_Prices]
ALTER COLUMN price NUMERIC(15,2)
ALTER COLUMN [Date] DATE

ALTER TABLE [Shoprite_Prices]
ALTER COLUMN price NUMERIC(15,2)
ALTER COLUMN [Date] DATE

ALTER TABLE woolworths_Prices
ALTER COLUMN price NUMERIC(15,2)
ALTER COLUMN [Date] DATE

/*
update [Fresh_Produce_Market_Data].[dbo].[PickNPay_Prices]
MTD_total_value_sold = CONVERT(NUMERIC(17,2),REPLACE(SUBSTRING([total_value_sold],CHARINDEX(':', [total_value_sold])+3,20),',',''))

--select cast([MTD_total_value_sold] as int) from [commodity_raw]
*/