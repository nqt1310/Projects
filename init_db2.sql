CREATE TABLE IF NOT EXISTS public.datadictionary (
    id SERIAL PRIMARY KEY,
    dataelement VARCHAR(255) NOT NULL, 
    description varchar(255) not null,
    legal_cons varchar(5000) not null,
    datatype varchar(5000) not null,
    PII_status varchar(5) not null,
    confidential_level varchar(10) not null,
    associated_businessterm varchar(20) not null
);

INSERT INTO public.datadictionary (dataelement, description, legal_cons, datatype, PII_status, confidential_level, associated_businessterm) VALUES
('PersonalIdentity', 'Số Giấy tờ tùy thân khách hàng', 'legal_cons_11', 'float', 'Y', 'public', 'Khả năng thanh toán lãi vay'),
('', 'description_11', 'legal_cons_11', 'float', 'Y', 'public', 'Khả năng thanh toán lãi vay'),
;
