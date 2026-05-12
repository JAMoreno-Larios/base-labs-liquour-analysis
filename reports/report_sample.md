
Annie's Magic Numbers Code Challenge
====================================

# Introduction



    The requirements for this report are to find out the following:
        
- Top 10 brands based on profits and margins
- Top 10 vendors based on profits and margins
- Which brands and vendors to drop due loses.



    For this analysis, we will calculate the profits using the Cost Of Goods Sold (COGS) metric. In this way we can determine our best-selling brands and vendors.
    
    From our SQL database exploration (refer to `notebooks/sql_columns_exploration.ipynb`), we do need to calculate two different COGS metrics: the full equation for the per-brand metrics, and a purchases-only COGS for the per-vendor one since the inventory tables do not contain vendor-specific information.
    
    The full accounting COGS formula is:
    $$COGS = Initial Inventory Value + Purchases + Freight Costs - Final Inventory Value$$
    
    Then, the profit is:
    $$Profit = Revenue - COGS$$
    
    Thus, the margins are:
    $$Margins = (Revenue - COGS) / Revenue * 100 [%]$$
    
    We'll explain a bit more in the following sections.
        
# Top 10 brands



    Freight costs are considered as a per-invoice basis, the data on the sales and purchases tables are shown as per-store.
    We will aggregate this information into a per-brand basis so we can account for a proportional freight allocation for
    the COGS calculation.
    
    From exploring the SQL tables, we identified that the brand refers to a single product type.
    
## Per profits


|   Brand | Description                  |   Total Revenue [USD] |   COGS [USD] |   Profit [USD] |   Margin [%] |
|---------|------------------------------|-----------------------|--------------|----------------|--------------|
|    1233 | Jack Daniels No 7 Black      |          5,101,919.51 | 3,751,050.18 |   1,350,869.33 |        26.48 |
|    3545 | Ketel One Vodka              |          4,223,107.62 | 2,988,900.72 |   1,234,206.90 |        29.23 |
|    4261 | Capt Morgan Spiced Rum       |          4,475,972.88 | 3,257,281.80 |   1,218,691.08 |        27.23 |
|    8068 | Absolut 80 Proof             |          4,538,120.60 | 3,430,854.00 |   1,107,266.60 |        24.40 |
|    3405 | Tito's Handmade Vodka        |          4,819,073.49 | 3,735,514.13 |   1,083,559.36 |        22.48 |
|    6570 | Kendall Jackson Chard Vt RSV |          2,326,007.78 | 1,457,832.10 |     868,175.68 |        37.32 |
|    3858 | Grey Goose Vodka             |          3,383,912.40 | 2,533,422.70 |     850,489.70 |        25.13 |
|    3489 | Tanqueray                    |          2,640,491.19 | 1,885,372.99 |     755,118.20 |        28.60 |
|    1376 | Jim Beam                     |          2,435,393.39 | 1,753,061.45 |     682,331.94 |        28.02 |
|    2663 | Dewars White Label           |          2,189,368.78 | 1,509,545.45 |     679,823.33 |        31.05 |


## Per margins

### Naive run - no purchases done in the period


|   Brand | Description                  |   Total Revenue [USD] |   COGS [USD] |   Profit [USD] |   Margin [%] |
|---------|------------------------------|-----------------------|--------------|----------------|--------------|
|    1099 | Angel's Envy NH Blend Bourbn |           6,346.62    |         0.00 |    6,346.62    |       100.00 |
|    1202 | Hennessy VS Chain VAP        |                191.94 |         0.00 |         191.94 |       100.00 |
|    2166 | The Macallan Double Cask 12  |          98,245.68    |         0.00 |   98,245.68    |       100.00 |
|    4164 | Hennessey 250 Collectors Edi |           1,199.98    |         0.00 |    1,199.98    |       100.00 |
|   18266 | Gianni Gagliardo Barolo 08   |                 95.98 |         0.00 |          95.98 |       100.00 |
|   20275 | Louis Jadot Les Drazeys 11   |                 73.98 |         0.00 |          73.98 |       100.00 |
|   20680 | A Bichot Champs Martin       |                245.94 |         0.00 |         245.94 |       100.00 |
|   22787 | Tenuta La Fuga 09 Brun Montl |                199.96 |         0.00 |         199.96 |       100.00 |
|   23048 | Dom Sigalas 11 Nychteri Assy |                124.95 |         0.00 |         124.95 |       100.00 |
|   33967 | Prunotto Bric Touro Barbesco |           3,617.14    |         0.00 |    3,617.14    |       100.00 |


### Considering if brand was ordered in the period


|   Brand | Description                 |   Total Revenue [USD] |    COGS [USD] |   Profit [USD] |   Margin [%] |
|---------|-----------------------------|-----------------------|---------------|----------------|--------------|
|    5335 | Beniotome Sesame Shochu     |           4,768.41    |         22.32 |    4,746.09    |        99.53 |
|   41231 | Mad Dogs & Englishmen Jumil |                279.80 |          6.56 |         273.24 |        97.65 |
|    1020 | B & B Dom VAP               |           1,319.48    |         36.40 |    1,283.08    |        97.24 |
|   20682 | A Bichot Chablis Vaucopins  |           1,623.44    |         59.88 |    1,563.56    |        96.31 |
|   39461 | Stags Leap SLV Cab Svgn     |           7,034.33    |        416.53 |    6,617.80    |        94.08 |
|    1414 | Bacardi 8 Gift Set          |                869.65 |         71.76 |         797.89 |        91.75 |
|    1214 | Apple Orchard Liqueur       |           2,017.98    |        198.59 |    1,819.39    |        90.16 |
|    2626 | Crown Royal Apple           |                 27.86 |          2.85 |          25.01 |        89.75 |
|   18130 | Castello Di Ama Chianti     |           3,107.16    |        324.44 |    2,782.72    |        89.56 |
|   37421 | Stags Leap Csk 23 Cab Svgn  |          11,714.29    |   1,399.92    |   10,314.37    |        88.05 |


## Losing brands


|   Brand | Description                  |   Total Revenue [USD] |    COGS [USD] |   Profit [USD] |   Margin [%] |
|---------|------------------------------|-----------------------|---------------|----------------|--------------|
|   25588 | High Valley Znfdl            |          55,406.43    |  80,577.58    |     -25,171.15 |       -45.43 |
|   26710 | Feudi Di San Gregorio Fiano  |          26,032.05    |  46,489.42    |     -20,457.37 |       -78.59 |
|    4300 | BenRiach Barrel 94           |           5,039.72    |  20,444.02    |     -15,404.30 |      -305.66 |
|   44714 | Buehler Znfdl Napa           |            119,616.75 |    134,791.91 |     -15,175.16 |       -12.69 |
|   33331 | Moletto Prosecco Della Marc  |          65,065.64    |  78,043.65    |     -12,978.01 |       -19.95 |
|   10666 | Clayhouse Adobe Cntrl Cst Wh |          31,188.64    |  43,857.22    |     -12,668.58 |       -40.62 |
|   19735 | Beringer Quantum Red Napa Vl |          31,159.68    |  43,524.98    |     -12,365.30 |       -39.68 |
|    1297 | Jim Beam Black               |          18,811.74    |  30,093.79    |     -11,282.05 |       -59.97 |
|    1361 | BenRiach 1994                |          12,919.32    |  23,335.70    |     -10,416.38 |       -80.63 |
|   25508 | Sbragia Zin Ginos Vyd- Dry C |          32,597.88    |  42,098.74    |   -9,500.86    |       -29.15 |
|    1095 | Southern Comfort wShaker     |           4,574.73    |  12,795.44    |   -8,220.71    |      -179.70 |
|     749 | Stolichnaya Hot Vodka        |          16,683.75    |  24,797.24    |   -8,113.49    |       -48.63 |
|   21505 | Margaride's Chard Arinto     |          23,891.88    |  31,997.10    |   -8,105.22    |       -33.92 |
|    6881 | Midnight Moon Cranberry      |          52,734.89    |  59,987.44    |   -7,252.55    |       -13.75 |
|   33982 | Lyeth Estate Meritage N Cst  |          58,140.95    |  65,168.55    |   -7,027.60    |       -12.09 |
|    2277 | Kilbeggan Irish Whiskey      |          20,272.54    |  26,696.71    |   -6,424.17    |       -31.69 |
|   25554 | Brotte Espirit CdR           |          42,674.68    |  48,995.88    |   -6,321.20    |       -14.81 |
|   25797 | GH Mumm Rose                 |          24,941.80    |  31,236.38    |   -6,294.58    |       -25.24 |
|    5270 | Southern Comfort             |          49,291.31    |  54,951.52    |   -5,660.21    |       -11.48 |
|    4606 | Grand Mayan Barrel Aged Tequ |          11,199.20    |  16,759.64    |   -5,560.44    |       -49.65 |


## Brand Analysis - Key Results

### High Vodka and Whiskey sales drive most of the profit



    Most of the profits are driven by high-volume sales, which are reflected on the first table.
    From it, we can see that four Vodka brands and three Whiskey bands dominate the leaderboard.
        
### '100%' margins are inventory runoff



    Brands that have 100% margin over this period are because no purchases were made.
    Sales were made from existing stock, which means that these margins are an data artifact.
        
### High margins correspond to low-volume items



    Brands with 90%+ margins correspond to tiny revenue scales. This is caused by existing inventory with minimal restocking.
    These products are not scalable profit drivers.
        
### Losing brands reflect a change in consumer taste



    Most of the losing brands in the period are wines with high COGS, suggesting that Annie's may have
    overprovisioned the stock for the season.
    We'd recommend to not order new stock on the losing brands until their COGS value gets lower in future months.
        
# Top 10 brands



    Since both beggining and end inventory tables do not have information regarding the vendor, we cannot use the
    full accounting formula.
    Instead we use the purchase-based COGS:
        COGS_vendor = Purchases_vendor + Freight_vendor
    
## Per profits


|   Vendor ID | Vendor Name                |   Total Revenue [USD] |   Purchase COGS [USD] |   Profit [USD] |   Margin [%] |
|-------------|----------------------------|-----------------------|-----------------------|----------------|--------------|
|        3960 | DIAGEO NORTH AMERICA INC   |         68,742,416.99 |         51,216,828.92 |  17,525,588.07 |        25.49 |
|        4425 | MARTIGNETTI COMPANIES      |         41,047,306.30 |         27,966,193.83 |  13,081,112.47 |        31.87 |
|        1392 | CONSTELLATION BRANDS INC   |         24,469,172.93 |         15,653,446.89 |   8,815,726.04 |        36.03 |
|       17035 | PERNOD RICARD USA          |         32,281,247.95 |         24,247,871.78 |   8,033,376.17 |        24.89 |
|       12546 | JIM BEAM BRANDS COMPANY    |         31,906,320.54 |         24,327,032.02 |   7,579,288.52 |        23.75 |
|         480 | BACARDI USA INC            |         25,014,556.89 |         17,713,664.99 |   7,300,891.90 |        29.19 |
|        3252 | E & J GALLO WINERY         |         18,556,085.61 |         12,351,575.00 |   6,204,510.61 |        33.44 |
|        1128 | BROWN-FORMAN CORP          |         18,478,557.47 |         13,598,034.76 |   4,880,522.71 |        26.41 |
|        9165 | ULTRA BEVERAGE COMPANY LLP |         17,822,938.45 |         13,278,668.63 |   4,544,269.82 |        25.50 |
|        9552 | M S WALKER INC             |         15,465,247.75 |         10,991,369.12 |   4,473,878.63 |        28.93 |


## Per margins

### Naive run - no purchases done in the period


|   Vendor ID | Vendor Name               |   Total Revenue [USD] |   Purchase COGS [USD] |   Profit [USD] |   Margin [%] |
|-------------|---------------------------|-----------------------|-----------------------|----------------|--------------|
|        1002 | BERNIKO LLC               |                 16.99 |                  0.00 |          16.99 |       100.00 |
|        9710 | WHYTE & MACKAY            |                 31.98 |                  0.00 |          31.98 |       100.00 |
|       90034 | EXCLUSIVE WINES & SPIRITS |                 55.98 |                  0.00 |          55.98 |       100.00 |
|      201359 | FLAVOR ESSENCE INC        |           1,474.41    |                 17.09 |    1,457.32    |        98.84 |
|       90026 | SILVER MOUNTAIN CIDERS    |                381.48 |                 77.54 |         303.94 |        79.67 |
|        1439 | CAPSTONE INTERNATIONAL    |                246.87 |                 54.91 |         191.96 |        77.76 |
|        1703 | ALISA CARR BEVERAGES      |            118,167.38 |          35,123.68    |   83,043.70    |        70.28 |
|        8663 | STAR INDUSTRIES INC.      |           7,914.72    |           2,464.73    |    5,449.99    |        68.86 |
|       90037 | THE PIERPONT GROUP LLC    |          17,937.21    |           5,741.17    |   12,196.04    |        67.99 |
|        7749 | R.P.IMPORTS INC           |          54,266.62    |          18,868.37    |   35,398.25    |        65.23 |


### Considering if we ordered from a given vendor during the period


|   Vendor ID | Vendor Name                 |   Total Revenue [USD] |   Purchase COGS [USD] |   Profit [USD] |   Margin [%] |
|-------------|-----------------------------|-----------------------|-----------------------|----------------|--------------|
|      201359 | FLAVOR ESSENCE INC          |           1,474.41    |                 17.09 |    1,457.32    |        98.84 |
|       90026 | SILVER MOUNTAIN CIDERS      |                381.48 |                 77.54 |         303.94 |        79.67 |
|        1439 | CAPSTONE INTERNATIONAL      |                246.87 |                 54.91 |         191.96 |        77.76 |
|        1703 | ALISA CARR BEVERAGES        |            118,167.38 |          35,123.68    |   83,043.70    |        70.28 |
|        8663 | STAR INDUSTRIES INC.        |           7,914.72    |           2,464.73    |    5,449.99    |        68.86 |
|       90037 | THE PIERPONT GROUP LLC      |          17,937.21    |           5,741.17    |   12,196.04    |        67.99 |
|        7749 | R.P.IMPORTS INC             |          54,266.62    |          18,868.37    |   35,398.25    |        65.23 |
|       90033 | FANTASY FINE WINES CORP     |                327.59 |                129.25 |         198.34 |        60.55 |
|        9751 | VINEDREA WINES LLC          |          11,385.60    |           4,682.13    |    6,703.47    |        58.88 |
|        2396 | BLACK PRINCE DISTILLERY INC |          11,818.85    |           6,002.92    |    5,815.93    |        49.21 |


## Losing Vendors


|   Vendor ID | Vendor Name                   |   Total Revenue [USD] |   Purchase COGS [USD] |   Profit [USD] |    Margin [%] |
|-------------|-------------------------------|-----------------------|-----------------------|----------------|---------------|
|          60 | ADAMBA IMPORTS INTL INC       |          67,576.22    |          77,137.77    |   -9,561.55    |        -14.15 |
|       90059 | BLACK COVE BEVERAGES          |           6,256.87    |          14,539.90    |   -8,283.03    |       -132.38 |
|           2 | IRA GOLDMAN AND WILLIAMS, LLP |           1,265.58    |           5,657.96    |   -4,392.38    |       -347.06 |
|        3951 | HIGHLAND WINE MERCHANTS LLC   |           1,533.68    |           5,529.75    |   -3,996.07    |       -260.55 |
|        6280 | UNCORKED                      |           1,124.38    |           2,981.57    |   -1,857.19    |       -165.17 |
|        3551 | GILMANTON WINERY & VINEYARD   |           3,837.60    |           5,419.67    |   -1,582.07    |        -41.23 |
|        5083 | LOYAL DOG WINERY              |           1,111.26    |           2,331.48    |   -1,220.22    |       -109.81 |
|      173357 | TAMWORTH DISTILLING           |          40,021.12    |          41,238.94    |   -1,217.82    |         -3.04 |
|         287 | APPOLO VINEYARDS LLC          |           1,616.92    |           2,411.98    |        -795.06 |        -49.17 |
|       99166 | STARK BREWING COMPANY         |          25,371.54    |          26,091.13    |        -719.59 |         -2.84 |
|       10050 | Russian Standard Vodka        |            139,327.43 |            139,639.87 |        -312.44 |         -0.22 |
|        9099 | TRUETT HURST                  |                 14.99 |                237.89 |        -222.90 |  -1,486.99    |


## Vendor Analysis - Key Results

### Diageo and Martignetti dominate profits



    Diageo North America generates 17.5 million in profit; Martignetti Companies, 13.1 million.
    These two companies represent the 37.12640777265981% of the top 10 earners.
    
### Losing vendors are small contributors



    All losing vendors are small producers with revenue under 70k. The only company worth reviewing are
    Adamba Imports (67.6k revenue, -9.6k loss).
    
### No major vendor relationships need termination



    All 10 profit-driving vendors are healthy. Losing vendor losses can be either ignored or fixed through pricing.
    