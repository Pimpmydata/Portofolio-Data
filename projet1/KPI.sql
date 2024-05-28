--KPI CA par pays 2 derniers mois
SELECT  sum(od.`quantityOrdered` * od.`priceEach`) as Total_CA, offi.country
FROM customers c
JOIN orders o on o.`customerNumber`=c.`customerNumber`
JOIN orderdetails od on od.`orderNumber`=o.`orderNumber`
JOIN employees e on e.`employeeNumber`=c.`salesRepEmployeeNumber`
JOIN offices as offi on offi.`officeCode`=e.`officeCode`
WHERE o.orderDate >=  DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
group by offi.country
order by Total_CA DESC;

--CA des deux derniers mois vs N-1 sur la même période
SELECT
    SUM(od.quantityOrdered * od.priceEach) as Total_CA,
    offi.country as pays,
    total_ca_pyear.total_ca_pyear AS Total_CA_Prec,
    CONCAT(ROUND((SUM(od.quantityOrdered * od.priceEach) - total_ca_pyear.total_ca_pyear)/total_ca_pyear.total_ca_pyear*100,1),"%") as progression,
    offi.territory as continent,
    c.customerName as client
FROM
    customers c
JOIN
    orders o ON o.customerNumber = c.customerNumber
JOIN
    orderdetails od ON od.orderNumber = o.orderNumber
JOIN
    employees e ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN
    offices AS offi ON offi.officeCode = e.officeCode
LEFT JOIN
    (SELECT
         SUM(od.quantityOrdered * od.priceEach) AS total_ca_pyear,
         offices.country
     FROM
         customers c
     JOIN
         orders o ON o.customerNumber = c.customerNumber
     JOIN
         orderdetails od ON od.orderNumber = o.orderNumber
     JOIN
         employees e ON e.employeeNumber = c.salesRepEmployeeNumber
     JOIN
         offices ON offices.officeCode = e.officeCode
     WHERE
         o.orderDate BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 14 MONTH) AND DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
     GROUP BY
         offices.country) AS total_ca_pyear ON offi.country = total_ca_pyear.country
WHERE
    o.orderDate >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
GROUP BY
    offi.country, offi.territory, client
ORDER BY
    Total_CA DESC;

--Origine des clients par pays, region
SELECT  c.country as pays_clients, offi.territory as region_vente, count(c.customerNumber) as nb_clients
FROM customers c
JOIN employees e on e.`employeeNumber`=c.`salesRepEmployeeNumber`
JOIN offices as offi on offi.`officeCode`=e.`officeCode`
GROUP BY c.country, offi.territory
ORDER BY nb_clients DESC, region_vente;

--Origine des clients par pays, agence
SELECT  c.country as pays_clients, offi.city as agence, count(c.customerNumber) as nb_clients
FROM customers c
join employees e on e.`employeeNumber`=c.`salesRepEmployeeNumber`
join offices as offi on offi.`officeCode`=e.`officeCode`
group by c.country, agence
order by nb_clients DESC, agence;

--CA par région, année
SELECT SUM(`quantityOrdered`*`priceEach`) as Total_CA, o.territory as region, YEAR(orders.orderDate) as annee
FROM orders
JOIN orderdetails on orderdetails.`orderNumber`=orders.`orderNumber`
JOIN customers on customers.`customerNumber`=orders.`customerNumber`
JOIN employees e on e.employeeNumber=customers.salesRepEmployeeNumber
JOIN offices o on o.officeCode=e.officeCode
WHERE orders.status <> "Cancelled"
GROUP BY YEAR(orders.orderDate), region
ORDER BY annee DESC, Total_CA DESC;

-- CA par agence, par année
SELECT SUM(`quantityOrdered`*`priceEach`) as Total_CA, o.city as agence, YEAR(orders.orderDate) as annee
FROM orders
JOIN orderdetails on orderdetails.`orderNumber`=orders.`orderNumber`
JOIN customers on customers.`customerNumber`=orders.`customerNumber`
JOIN employees e on e.employeeNumber=customers.salesRepEmployeeNumber
JOIN offices o on o.officeCode=e.officeCode
GROUP BY YEAR(orders.orderDate), agence
ORDER BY annee DESC, Total_CA DESC;

-- 10 premiers clients en dépassement de limite de crédit v1
select p.paymentDate, p.amount as total_paiements, c.customerName, sum(o2.priceEach*o2.quantityOrdered) as amount_ordered,
(sum(o2.priceEach*o2.quantityOrdered)-p.amount) as credit_client, c.creditLimit,
CASE WHEN (sum(o2.priceEach*o2.quantityOrdered)-p.amount) > creditLimit THEN "Limite dépassée"
	 WHEN (sum(o2.priceEach*o2.quantityOrdered)-p.amount) <=  creditLimit THEN "Ok"
END as depassement, (sum(o2.priceEach*o2.quantityOrdered)-p.amount-creditLimit) as montant_depassement
FROM customers c
JOIN payments p on p.customerNumber = c.customerNumber
JOIN orders o on o.customerNumber = c.customerNumber
JOIN orderdetails o2 on o2.orderNumber = o.orderNumber
WHERE p.paymentDate >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
GROUP BY p.paymentDate, p.amount, c.customerName, c.creditLimit
ORDER BY (sum(o2.priceEach*o2.quantityOrdered)-p.amount-creditLimit) DESC
LIMIT 10

--v2
WITH TotalCommands AS (
    SELECT c.customerName, SUM(o2.priceEach * o2.quantityOrdered) AS total_cmde, SUBSTR(c.customerName, 1, 18) as cust_shortname18
    FROM customers c
    LEFT JOIN orders o ON o.customerNumber = c.customerNumber AND o.status <> 'Cancelled'
    LEFT JOIN orderdetails o2 ON o2.orderNumber = o.orderNumber
    GROUP BY c.customerName),
	TotalPayments AS (
	SELECT c.customerName, SUM(p.amount) AS total_paiement, SUBSTRING(c.customerName, 1, 10) as cust_shortname
	FROM customers c
	LEFT JOIN payments p ON p.customerNumber = c.customerNumber
	GROUP BY c.customerName),
	creditlimit as(
	SELECT c.creditLimit, c.customerName, SUBSTRING(c.customerName, 0, 10) as cust_shortname
	FROM customers c)
SELECT COALESCE(TotalCommands.customerName, TotalPayments.customerName) AS customerName,
TotalCommands.cust_shortname18,
SUBSTRING(TotalCommands.cust_shortname18, 1, 10) as cust_shortname10,
COALESCE(TotalCommands.total_cmde, 0) AS total_cmde,
COALESCE(TotalPayments.total_paiement, 0) AS total_paiement,
COALESCE (TotalCommands.total_cmde - TotalPayments.total_paiement, 0) as encours,
creditlimit.creditLimit,
COALESCE ((TotalCommands.total_cmde - TotalPayments.total_paiement)/creditlimit.creditLimit*100, 0) as taux_utl_limite_val
CONCAT(COALESCE ((TotalCommands.total_cmde - TotalPayments.total_paiement)/creditlimit.creditLimit*100, 0),"%") as taux_utl_limite
FROM TotalCommands
LEFT JOIN TotalPayments ON TotalCommands.customerName = TotalPayments.customerName
LEFT JOIN creditlimit ON creditlimit.customerName = TotalCommands.customerName;

--CA par catégorie de produit 3 derniers mois glissant
SELECT p.`productLine`, sum(od.`quantityOrdered`*od.`priceEach`) as CA,
CASE WHEN MONTH(o.`orderDate`)=1 THEN "Janvier"
     when MONTH(o.`orderDate`)=2 THEN "Février"
     WHEN MONTH(o.`orderDate`)=3 THEN "Mars"
     when MONTH(o.`orderDate`)=4 THEN "Avril"
     WHEN MONTH(o.`orderDate`)=5 THEN "Mai"
     when MONTH(o.`orderDate`)=6 THEN "Juin"
     WHEN MONTH(o.`orderDate`)=7 THEN "Juillet"
     when MONTH(o.`orderDate`)=8 THEN "Août"
     WHEN MONTH(o.`orderDate`)=9 THEN "Septembre"
     when MONTH(o.`orderDate`)=10 THEN "Octobre"
     WHEN MONTH(o.`orderDate`)=11 THEN "Novembre"
     when MONTH(o.`orderDate`)=12 THEN "Décembre"
     else "Erreur"
END as mois, YEAR(o.`orderDate`) as annee
FROM orderdetails as od
JOIN products p on p.`productCode`=od.`productCode`
JOIN orders o on o.`orderNumber`=od.`orderNumber`
WHERE o.orderDate >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
GROUP BY p.`productLine`, o.`orderDate`
ORDER BY YEAR(o.`orderDate`) DESC, MONTH(o.`orderDate`) DESC;

