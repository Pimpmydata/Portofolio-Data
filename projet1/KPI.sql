SELECT  sum(od.`quantityOrdered` * od.`priceEach`) as Total_CA, offi.country
FROM customers c
JOIN orders o on o.`customerNumber`=c.`customerNumber`
JOIN orderdetails od on od.`orderNumber`=o.`orderNumber`
JOIN employees e on e.`employeeNumber`=c.`salesRepEmployeeNumber`
JOIN offices as offi on offi.`officeCode`=e.`officeCode`
WHERE o.orderDate >=  DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)
group by offi.country
order by Total_CA DESC;