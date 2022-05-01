select (
select count(*) from "Invoice" where "InvoiceDate"::text like '2009-01%' ) as TotalInvoicesIn2009, (
select count(*) from "Invoice" where "InvoiceDate"::text like '2011-01%')  as TotalInvoicesIn2011