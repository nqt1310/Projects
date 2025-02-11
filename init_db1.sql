CREATE TABLE IF NOT EXISTS public.businessglossary (
    id SERIAL PRIMARY KEY,
    businessterm VARCHAR(255) NOT NULL, 
    description varchar(255) not null,
    abbreviation varchar(5000) not null,
    link_asset varchar(5000) not null 
);

INSERT INTO public.newtable (namedest) VALUES
(1,'OneID','Dự án hợp nhất khách hàng tập đoàn','OneID','Conf OneID Home'),
(2,'Hệ số thanh toán ngắn hạn','Đánh giá khả năng thanh toán các khoản nợ ngắn hạn bằng tài sản ngắn hạn.','CR' ,null),
(3,'Hệ số thanh toán nhanh','Đánh giá khả năng thanh toán nợ ngắn hạn bằng tiền và các khoản tương đương tiền.', 'QR',null),
(4,'Khả năng thanh toán lãi vay',  'Đánh giá khả năng trả lãi vay từ lợi nhuận trước thuế và lãi.', 'TIE', null),
(5,'Hệ số tự tài trợ', 'Đánh giá mức độ tự chủ về tài chính của doanh nghiệp.','DER',  null),
(6,'Hệ số đòn bẩy tài chính','Thể hiện mối quan hệ giữa nguồn vốn vay và vốn chủ sở hữu.', 'FLR',  null ),
(7,'Tỷ suất lợi nhuận trên doanh thu','Đánh giá khả năng sinh lời từ doanh thu.', 'ROS',  null),
(8,'Tỷ suất lợi nhuận trên tài sản','Đánh giá khả năng sinh lời từ tổng tài sản.', 'ROA',  null),
(9,'Tỷ suất lợi nhuận trên vốn chủ sở hữu', 'Đánh giá khả năng sinh lời từ vốn chủ sở hữu.','ROE',  null)
(10,'Thông tin định danh khách hàng','Các thông tin GTTT, Giới tính, Địa chỉ, Họ tên, SĐT, Email','PII',null)
;