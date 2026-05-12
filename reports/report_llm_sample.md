
Annie's Magic Numbers Code Challenge - LLM insights
===================================================

# Introduction



We want to analyze the:
        
- Top 10 brands based on profits and margins
- Top 10 vendors based on profits and margins, and
- Which brands and vendors to drop due loses.



For this report, we present LLM-generated insights based on our processed data. 
        
# Top 3 actionable insights for Annie


## Top 3 Actionable Insights

### 1. Discontinue or Renegotiate High-Loss Brands
Several brands are generating significant losses that directly erode profitability. The top loss-makers include **High Valley Zinfandel** (-$25,171 at -45% margin), **Feudi Di San Gregorio Fiano** (-$20,457 at -79% margin), **BenRiach Barrel 94** (-$15,404 at -306% margin), and **Buehler Zinfandel Napa** (-$15,175 at -13% margin). Priority should be given to brands with extreme negative margins such as BenRiach Barrel 94 and Feudi Di San Gregorio Fiano, where COGS far exceed revenue. Annie should immediately review these SKUs for discontinuation or seek urgent price renegotiation with suppliers to bring margins into positive territory.

### 2. Address Underperforming Vendors with Structural Losses
Four vendors stand out as particularly damaging: **IRA GOLDMAN AND WILLIAMS, LLP** (-347% margin), **HIGHLAND WINE MERCHANTS LLC** (-261% margin), **BLACK COVE BEVERAGES** (-132% margin), and **UNCORKED** (-165% margin). These vendors show COGS dramatically exceeding revenue, suggesting either severe mispricing or unfavorable contract terms. Annie should consider terminating these vendor relationships or renegotiating cost structures. Additionally, **ADAMBA IMPORTS INTL INC** represents the largest absolute vendor loss (-$9,562), making it a priority for contract review.

### 3. Double Down on High-Profit, High-Margin Brands and Vendors
The data clearly shows where profitability is strongest. On the brand side, **Jack Daniels No. 7 Black** ($1.35M profit), **Ketel One Vodka** ($1.23M), and **Captain Morgan Spiced Rum** ($1.22M) lead in absolute profit. **Kendall Jackson Chardonnay VT RSV** stands out with the best margin among high-volume brands at 37.3%. On the vendor side, **DIAGEO NORTH AMERICA** ($17.5M profit) and **MARTIGNETTI COMPANIES** ($13.1M at 31.9% margin) are the strongest partners. Annie should prioritize expanding order volumes with these vendors and increasing shelf and marketing focus on these top-performing brands to maximize returns.
# Methodology



For this analysis, we will calculate the profits using the Cost Of Goods Sold (COGS) metric. In this way we can determine
our best-selling brands and vendors.
From our SQL database exploration (refer to `notebooks/sql_columns_exploration.ipynb`), we do need to calculate two different
COGS metrics: the full equation for the per-brand metrics, and a purchases-only COGS for the per-vendor one since
the inventory tables do not contain vendor-specific information.

The full accounting COGS formula is:
$$COGS = Initial Inventory Value + Purchases + Freight Costs - Final Inventory Value$$

Then, the profit is:
$$Profit = Revenue - COGS$$

Thus, the margins are:
$$Margins = (Revenue - COGS) / Revenue * 100 [%]$$

We found out that we cannot use the full accounting COGS formula for our vendor-based analysis since there is
no vendor data in the inventory tables, thus, we use a modified COGS formula to estimate profits:

    $$COGS_vendor = Purchases_vendor + Freight_vendor$$

        
# Supporting data



Freight costs are considered as a per-invoice basis, the data on the sales and purchases tables are shown as per-store.
We will aggregate this information into a per-brand basis so we can account for a proportional freight allocation for
the COGS calculation.

From exploring the SQL tables, we identified that the brand refers to a single product type.
    
## Top 10 brands

### Per profits


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


### Per margins

#### Naive run - no purchases done in the period


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


#### Considering if brand was ordered in the period


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


### Losing brands


|   Brand | Description                   |   Total Revenue [USD] |    COGS [USD] |   Profit [USD] |   Margin [%] |
|---------|-------------------------------|-----------------------|---------------|----------------|--------------|
|   25588 | High Valley Znfdl             |          55,406.43    |  80,577.58    |     -25,171.15 |       -45.43 |
|   26710 | Feudi Di San Gregorio Fiano   |          26,032.05    |  46,489.42    |     -20,457.37 |       -78.59 |
|    4300 | BenRiach Barrel 94            |           5,039.72    |  20,444.02    |     -15,404.30 |      -305.66 |
|   44714 | Buehler Znfdl Napa            |            119,616.75 |    134,791.91 |     -15,175.16 |       -12.69 |
|   33331 | Moletto Prosecco Della Marc   |          65,065.64    |  78,043.65    |     -12,978.01 |       -19.95 |
|   10666 | Clayhouse Adobe Cntrl Cst Wh  |          31,188.64    |  43,857.22    |     -12,668.58 |       -40.62 |
|   19735 | Beringer Quantum Red Napa Vl  |          31,159.68    |  43,524.98    |     -12,365.30 |       -39.68 |
|    1297 | Jim Beam Black                |          18,811.74    |  30,093.79    |     -11,282.05 |       -59.97 |
|    1361 | BenRiach 1994                 |          12,919.32    |  23,335.70    |     -10,416.38 |       -80.63 |
|   25508 | Sbragia Zin Ginos Vyd- Dry C  |          32,597.88    |  42,098.74    |   -9,500.86    |       -29.15 |
|    1095 | Southern Comfort wShaker      |           4,574.73    |  12,795.44    |   -8,220.71    |      -179.70 |
|     749 | Stolichnaya Hot Vodka         |          16,683.75    |  24,797.24    |   -8,113.49    |       -48.63 |
|   21505 | Margaride's Chard Arinto      |          23,891.88    |  31,997.10    |   -8,105.22    |       -33.92 |
|    6881 | Midnight Moon Cranberry       |          52,734.89    |  59,987.44    |   -7,252.55    |       -13.75 |
|   33982 | Lyeth Estate Meritage N Cst   |          58,140.95    |  65,168.55    |   -7,027.60    |       -12.09 |
|    2277 | Kilbeggan Irish Whiskey       |          20,272.54    |  26,696.71    |   -6,424.17    |       -31.69 |
|   25554 | Brotte Espirit CdR            |          42,674.68    |  48,995.88    |   -6,321.20    |       -14.81 |
|   25797 | GH Mumm Rose                  |          24,941.80    |  31,236.38    |   -6,294.58    |       -25.24 |
|    5270 | Southern Comfort              |          49,291.31    |  54,951.52    |   -5,660.21    |       -11.48 |
|    4606 | Grand Mayan Barrel Aged Tequ  |          11,199.20    |  16,759.64    |   -5,560.44    |       -49.65 |
|   13338 | C'est La Vie Pnt Nr/Syrh VDP  |          31,896.11    |  37,408.46    |   -5,512.35    |       -17.28 |
|    4277 | Bacardi Limon Rum             |          46,397.94    |  51,805.25    |   -5,407.31    |       -11.65 |
|    2590 | The Black Grouse Scotch       |          77,304.21    |  82,635.02    |   -5,330.81    |        -6.90 |
|    1927 | Jack Daniels Barrel Proof     |          89,296.41    |  94,308.58    |   -5,012.17    |        -5.61 |
|   43937 | P Jaboulet Hrmtg 10 Chapelle  |                951.96 |   5,369.93    |   -4,417.97    |      -464.09 |
|    2040 | Malfy Gin Con Limone          |          19,909.42    |  24,233.12    |   -4,323.70    |       -21.72 |
|   25827 | Angeline Cab Svgn California  |          18,956.13    |  23,200.05    |   -4,243.92    |       -22.39 |
|   13339 | C'Est La Vie Chard/Svgn Bl    |          31,434.71    |  35,666.12    |   -4,231.41    |       -13.46 |
|     814 | Sammy's Beach Bar Rum         |          10,306.06    |  14,414.69    |   -4,108.63    |       -39.87 |
|   21003 | Bonpas Ventoux Rouge Rhone    |          26,604.80    |  30,700.69    |   -4,095.89    |       -15.40 |
|   25937 | Cavit Select Red Blend        |           6,526.31    |  10,590.16    |   -4,063.85    |       -62.27 |
|   25857 | Cline Merlot Sonoma Coast     |          19,111.96    |  23,174.85    |   -4,062.89    |       -21.26 |
|    1081 | Chivas Regal with2 50mLs      |          23,158.41    |  27,053.29    |   -3,894.88    |       -16.82 |
|    2734 | Nikka Pure Malt whiskey       |          49,549.72    |  53,378.15    |   -3,828.43    |        -7.73 |
|    4366 | Kracken Black Rum             |          38,626.26    |  42,364.06    |   -3,737.80    |        -9.68 |
|    3375 | Skyy Infusions Cranberry      |          26,733.21    |  30,112.14    |   -3,378.93    |       -12.64 |
|   16189 | Frescobaldi Tenuta Castglni   |          42,959.38    |  46,066.71    |   -3,107.33    |        -7.23 |
|    3283 | New Amsterdam Apple Vodka     |          19,321.69    |  22,332.77    |   -3,011.08    |       -15.58 |
|   18572 | Butterfly Kiss Moscato        |           1,653.47    |   4,563.27    |   -2,909.80    |      -175.98 |
|   19996 | Inspired Red Blend CA         |          36,152.53    |  39,025.23    |   -2,872.70    |        -7.95 |
|   26377 | Orin Swift D66 Grenache Cata  |           9,950.31    |  12,677.92    |   -2,727.61    |       -27.41 |
|   25584 | Rex Hill Seven Soils Chard    |           8,894.29    |  11,473.07    |   -2,578.78    |       -28.99 |
|   26672 | Tridente Tempranillo Castila  |          18,947.03    |  21,510.97    |   -2,563.94    |       -13.53 |
|   46156 | Brookdale Cab Svgn Napa       |           5,847.06    |   8,302.36    |   -2,455.30    |       -41.99 |
|   22274 | Complicated Chard             |          15,367.38    |  17,800.44    |   -2,433.06    |       -15.83 |
|   25843 | Ch Bois du Fil Brdx           |           5,051.63    |   7,402.04    |   -2,350.41    |       -46.53 |
|   12910 | Drouhin Gevrey-Chambertin 13  |           2,107.66    |   4,455.71    |   -2,348.05    |      -111.41 |
|   27164 | Guillaume Vrignaud Chablis    |                674.75 |   2,978.62    |   -2,303.87    |      -341.44 |
|   20975 | Belle Ambiance Pnt Nr         |           8,228.50    |  10,525.63    |   -2,297.13    |       -27.92 |
|   25640 | Picket Fence Cab Svgn Alexan  |          11,101.11    |  13,309.73    |   -2,208.62    |       -19.90 |
|   25352 | Cecchi Chianti DOCG           |          15,899.24    |  18,100.73    |   -2,201.49    |       -13.85 |
|    2729 | Hell-Cat Maggie Irish Whisky  |          26,452.79    |  28,591.30    |   -2,138.51    |        -8.08 |
|   22583 | Cambria Julias Vyd Pnt Nr     |          44,194.12    |  46,190.54    |   -1,996.42    |        -4.52 |
|   20706 | A Proper Claret               |          45,443.73    |  47,427.21    |   -1,983.48    |        -4.36 |
|   24987 | Rock Wall 12 Monte Rosso Znf  |           3,159.21    |   5,116.06    |   -1,956.85    |       -61.94 |
|    3900 | Bracero Reposado Tequila      |          14,894.40    |  16,719.44    |   -1,825.04    |       -12.25 |
|   26361 | Prophecy Red Blend            |          13,830.78    |  15,456.08    |   -1,625.30    |       -11.75 |
|   38191 | Argiola Vermentino Costamol   |           8,970.11    |  10,472.30    |   -1,502.19    |       -16.75 |
|    1781 | Wild Turkey Russell's Rsv     |          49,045.73    |  50,513.51    |   -1,467.78    |        -2.99 |
|   25684 | Jekel Pnt Nr Monterey         |           3,405.76    |   4,832.50    |   -1,426.74    |       -41.89 |
|   18254 | Jaboulet 09 Dom Terre Ferme   |                431.94 |   1,840.70    |   -1,408.76    |      -326.15 |
|   17187 | The Messenger Telegram Red 2  |          39,487.14    |  40,852.76    |   -1,365.62    |        -3.46 |
|    7680 | Viniq Shimmery Glow           |          20,576.96    |  21,860.81    |   -1,283.85    |        -6.24 |
|    4876 | Skyy Infusion Tropical Mango  |          16,643.10    |  17,890.30    |   -1,247.20    |        -7.49 |
|   12913 | J Drouhin Vosne Romanee 13    |           4,664.51    |   5,898.59    |   -1,234.08    |       -26.46 |
|   23068 | Nicolas Perrin Cote Rotie 11  |                239.96 |   1,466.42    |   -1,226.46    |      -511.11 |
|   25936 | Roscato Rose Dolce            |           9,692.64    |  10,907.38    |   -1,214.74    |       -12.53 |
|   23891 | Cycles Gladiator Cab Svgn     |          14,927.86    |  16,092.14    |   -1,164.28    |        -7.80 |
|   12401 | Altos del Cuco Red            |           8,145.54    |   9,305.26    |   -1,159.72    |       -14.24 |
|    4053 | Bird Dog Strawberry Whiskey   |          18,130.74    |  19,245.19    |   -1,114.45    |        -6.15 |
|   22924 | Patricius Sarga Muskotaly     |           2,317.22    |   3,390.40    |   -1,073.18    |       -46.31 |
|   25216 | Castello D'Alba Vinho Tinta   |           8,209.00    |   9,234.65    |   -1,025.65    |       -12.49 |
|    1084 | Cointreau Liqueur with Carafe |          14,865.07    |  15,864.09    |        -999.02 |        -6.72 |
|    6136 | Casoni Limoncello di Sorento  |                833.99 |   1,735.35    |        -901.36 |      -108.08 |
|   13504 | New Age Valentin Bianchi Whi  |          11,894.53    |  12,790.28    |        -895.75 |        -7.53 |
|    3573 | Stoli Elite Vodka             |          18,798.01    |  19,678.80    |        -880.79 |        -4.69 |
|    3963 | Menage A Trois Vodka          |          19,342.40    |  20,197.20    |        -854.80 |        -4.42 |
|   44742 | Gamba Znfdl RRV Old Vine      |           1,692.59    |   2,544.81    |        -852.22 |       -50.35 |
|   26340 | Avancia 15 Cuvee De O Rose M  |           4,196.53    |   5,007.71    |        -811.18 |       -19.33 |
|   10121 | Columbia Crest 08 Cab Svgn    |           1,115.69    |   1,924.60    |        -808.91 |       -72.50 |
|    8337 | Marcati Limoncello            |          12,224.54    |  13,018.55    |        -794.01 |        -6.50 |
|   45837 | R Stemmler Nugent Pnt Nr      |           7,198.00    |   7,977.86    |        -779.86 |       -10.83 |
|   16776 | Amapola Creek Cab Svgn 10     |                338.97 |   1,088.19    |        -749.22 |      -221.03 |
|   22923 | Patricius Tokaj Harslevelu    |           2,344.48    |   3,091.47    |        -746.99 |       -31.86 |
|   18781 | Girl Go Lightly Moscato       |                618.20 |   1,362.00    |        -743.80 |      -120.32 |
|   14436 | Byron Santa Barbara Chard     |           2,422.30    |   3,139.35    |        -717.05 |       -29.60 |
|   24951 | Jackhammer Pnt Nr             |           6,097.06    |   6,807.66    |        -710.60 |       -11.65 |
|   23150 | Jekel Cab Svgn Monterey       |           1,649.59    |   2,351.56    |        -701.97 |       -42.55 |
|   17170 | Zeitgeist Cab Svgn Napa Vly   |           4,604.01    |   5,304.06    |        -700.05 |       -15.21 |
|   45246 | Shoofly Shiraz                |          38,679.82    |  39,372.25    |        -692.43 |        -1.79 |
|    2384 | Old Tahoe Straight Rye        |          10,220.52    |  10,902.57    |        -682.05 |        -6.67 |
|   19833 | Terra di Montevero Toscana    |           1,741.41    |   2,417.77    |        -676.36 |       -38.84 |
|   23170 | Marchesi di Barolo Sarmsa 07  |           1,139.85    |   1,790.49    |        -650.64 |       -57.08 |
|   25411 | Artesa Rsv Chard              |           2,724.72    |   3,369.10    |        -644.38 |       -23.65 |
|   22995 | Valckenberg Pinot Blanc       |           4,705.05    |   5,289.40    |        -584.35 |       -12.42 |
|   16726 | g Sake                        |                819.92 |   1,394.31    |        -574.39 |       -70.05 |
|    2762 | The Steward's Solera Bourbon  |          14,928.20    |  15,498.78    |        -570.58 |        -3.82 |
|    4092 | Bacardi Grapefruit Rum        |          11,529.27    |  12,095.03    |        -565.76 |        -4.91 |
|   26013 | Toad Hollow Cab Svgn Lodi     |          14,704.57    |  15,255.09    |        -550.52 |        -3.74 |
|    4102 | Bacardi Raspberry Rum         |          36,626.19    |  37,172.51    |        -546.32 |        -1.49 |
|   27172 | Pecchenino 12 Siri d'Jermu D  |           1,405.26    |   1,920.74    |        -515.48 |       -36.68 |
|   20429 | Carpineto Montepulciano 11    |           2,247.35    |   2,759.50    |        -512.15 |       -22.79 |
|    2405 | Old Tahoe Honey Rye           |           9,230.58    |   9,734.56    |        -503.98 |        -5.46 |
|   25376 | Artesa Rsv Pnt Nr             |           2,858.68    |   3,359.40    |        -500.72 |       -17.52 |
|    2874 | Hirsch 20 Yr American Whisky  |          28,994.28    |  29,450.07    |        -455.79 |        -1.57 |
|   23519 | Slow Press Chard              |           9,333.16    |   9,777.96    |        -444.80 |        -4.77 |
|    3542 | Vera Limon Vodka              |          23,414.54    |  23,837.94    |        -423.40 |        -1.81 |
|    4326 | Rumson's Coffee Rum           |          16,023.68    |  16,440.56    |        -416.88 |        -2.60 |
|   22922 | Patricius Tokaj Furmint       |           2,496.64    |   2,911.29    |        -414.65 |       -16.61 |
|   18430 | Bertani Secco 09 Edition IGT  |           2,973.53    |   3,359.55    |        -386.02 |       -12.98 |
|   24692 | Calmel & Joseph Chard         |           2,432.69    |   2,815.86    |        -383.17 |       -15.75 |
|   23936 | Morel Bjls-Vlgs Emeringes     |                951.35 |   1,308.15    |        -356.80 |       -37.50 |
|    3350 | Ice Fox Vodka                 |           6,569.40    |   6,919.15    |        -349.75 |        -5.32 |
|   17741 | Olivier Leflaive Bourg Al 12  |                113.94 |        459.09 |        -345.15 |      -302.93 |
|   15851 | Sextant Wheelhouse Znfdl      |                863.04 |   1,198.19    |        -335.15 |       -38.83 |
|   24696 | Black Stallion 10 Trans Cab   |                269.98 |        548.94 |        -278.96 |      -103.33 |
|   25608 | Artesa Elements Cab Svgn      |                544.36 |        819.52 |        -275.16 |       -50.55 |
|   15650 | Cuvee de Pena Rose            |           4,213.46    |   4,467.93    |        -254.47 |        -6.04 |
|   12518 | Raimat Vina 24 Albarino Whte  |                801.66 |   1,049.54    |        -247.88 |       -30.92 |
|   20724 | Spritz and Giggles            |           7,440.92    |   7,687.13    |        -246.21 |        -3.31 |
|   18947 | Austin Hope 10 Grenache       |           1,111.48    |   1,331.85    |        -220.37 |       -19.83 |
|    3574 | Stoli Gluten Free Vodka       |          12,068.48    |  12,255.09    |        -186.61 |        -1.55 |
|   22599 | Antica Fratta Franciacorta B  |           6,680.38    |   6,864.31    |        -183.93 |        -2.75 |
|   20596 | Aviary Cab Svgn               |                119.94 |        299.36 |        -179.42 |      -149.59 |
|   22661 | Iron Horse Est Brut Rose      |           1,722.39    |   1,884.89    |        -162.50 |        -9.43 |
|   24515 | Cartlidge & Browne Chard      |           3,952.27    |   4,093.77    |        -141.50 |        -3.58 |
|   23983 | King Estate Dom Pnt Nr 12     |           3,761.43    |   3,896.83    |        -135.40 |        -3.60 |
|   19760 | Rose'N'Blum Red Moscato       |                136.65 |        259.43 |        -122.78 |       -89.85 |
|   47049 | Argiola Turriga 05 Isola Nur  |                794.70 |        914.84 |        -120.14 |       -15.12 |
|    3432 | Capri Natura Limoncello       |           3,807.01    |   3,915.91    |        -108.90 |        -2.86 |
|    8090 | Russian Standard Gold Vodka   |           1,109.63    |   1,215.05    |        -105.42 |        -9.50 |
|   21180 | Amapola Creek Chard RR 14     |                551.70 |        651.60 |         -99.90 |       -18.11 |
|   15880 | San Polo Brun di Montlcno 11  |                149.98 |        246.26 |         -96.28 |       -64.20 |
|   22417 | Elouan Pnt Nr Oregon          |          18,610.71    |  18,706.64    |         -95.93 |        -0.52 |
|   12665 | Umberto Cesari Moma Red       |                235.72 |        329.59 |         -93.87 |       -39.82 |
|   20967 | Ninety Cellars Lot 106 Pnt N  |                175.89 |        266.07 |         -90.18 |       -51.27 |
|   22327 | Saved Rose                    |           1,388.01    |   1,475.65    |         -87.64 |        -6.31 |
|   18268 | Caprai Montefalco Rosso 09    |                813.32 |        897.42 |         -84.10 |       -10.34 |
|   41529 | Artesa Elements Napa Red      |                744.33 |        824.43 |         -80.10 |       -10.76 |
|   13676 | Scagliola Busiord Dolcetto    |                 44.92 |        110.32 |         -65.40 |      -145.59 |
|    2621 | Silo Bourbon                  |           2,137.58    |   2,197.22    |         -59.64 |        -2.79 |
|   27546 | NinetyCellars Lot 50 Prosec   |                259.87 |        315.28 |         -55.41 |       -21.32 |
|   22477 | Mionetto IL Moscato           |                747.06 |        800.83 |         -53.77 |        -7.20 |
|   21997 | Magnolia Court Merlot Paso R  |                258.63 |        312.11 |         -53.48 |       -20.68 |
|   38314 | Momokawa Silver Sake          |                899.04 |        950.78 |         -51.74 |        -5.76 |
|   27274 | Jos Phelps Insignia 13        |                209.99 |        258.96 |         -48.97 |       -23.32 |
|   23032 | Zenato Cresasso               |           2,149.57    |   2,195.51    |         -45.94 |        -2.14 |
|   22663 | Iron Horse Ocean Rsv Nationa  |                779.71 |        821.17 |         -41.46 |        -5.32 |
|   20798 | Belle Ambiance Red            |                 32.97 |         72.30 |         -39.33 |      -119.29 |
|   27342 | 19 Crimes The Banished Red    |                 38.97 |         73.49 |         -34.52 |       -88.57 |
|   19845 | The Rule Cab Svgn Napa Vly    |           5,026.20    |   5,055.63    |         -29.43 |        -0.59 |
|    2720 | Canadian Regal Apple          |          11,491.96    |  11,520.98    |         -29.02 |        -0.25 |
|   12650 | Harbor Town Svgn Bl           |          17,888.65    |  17,917.62    |         -28.97 |        -0.16 |
|   24546 | Selini Nano Svgn Bl           |           1,807.47    |   1,834.06    |         -26.59 |        -1.47 |
|   24478 | ZIPZ Cab Svgn                 |                139.62 |        160.65 |         -21.03 |       -15.06 |
|    2094 | Kilchoman Machir Bay Whiskey  |                133.98 |        154.62 |         -20.64 |       -15.40 |
|   35977 | Jaboulet Cotes du Rhone Par   |                159.89 |        179.65 |         -19.76 |       -12.36 |
|   18810 | C Y Toro Frontera Pnt Nr      |                 32.45 |         51.96 |         -19.51 |       -60.12 |
|   27553 | Hedges Family Estate Red Mtn  |                 26.99 |         38.40 |         -11.41 |       -42.26 |
|   26077 | Ninety Cellars Lot 129 Znfdl  |                 76.93 |         87.20 |         -10.27 |       -13.35 |
|   46929 | Lindemans Bin 85 Pnt Grigio   |                114.82 |        123.23 |          -8.41 |        -7.33 |
|   27969 | Fattoria le Pupille Poggio    |                 36.99 |         45.18 |          -8.19 |       -22.14 |
|   18655 | Keo Othello Cyprus Red        |                 75.91 |         83.97 |          -8.06 |       -10.62 |
|   16777 | Amapola Creek Znfdl 09        |                287.96 |        295.86 |          -7.90 |        -2.74 |
|   13557 | Merry Edwards Flax Vyd Pnt N  |                 69.99 |         74.21 |          -4.22 |        -6.03 |
|   22006 | Magnolia Court Chardonnay Ce  |                 55.92 |         59.44 |          -3.52 |        -6.29 |
|   22591 | Ch Manos Cadillac             |                 15.99 |         18.35 |          -2.36 |       -14.74 |
|   37422 | Stags Leap Fay Cab Svgn Napa  |           4,647.62    |   4,647.98    |          -0.36 |        -0.01 |
|   15901 | Merry Edwards Georg Pnt Nr    |                 79.99 |         80.05 |          -0.06 |        -0.07 |


## Top 10 vendors

### Per profits


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


### Per margins

#### Naive run - no purchases done in the period


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


#### Considering if we ordered from a given vendor during the period


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


### Losing Vendors


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

