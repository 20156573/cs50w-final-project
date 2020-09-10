# cs50w-final-project

Đây là trang web cho phép người dùng tìm kiếm nhà thuê, đăng tin cho thuê nhà, ngoài ra còn có thể nạp tiền vào trang web để đẩy tin và cho phép admin quản lý hệ thống như quản lý người dùng và tài chính, cũng như quản lý trạng hoạt động của các bài đăng cùng các yêu cầu từ người dùng đối với bài đăng của mình.

Đối tượng sử dụng: người dùng (có tài khoản, chưa có tài khoản), admin

Chức năng từng đối tượng: 

Người dùng chưa có tài khoản: Tìm kiếm thông tin nhà theo bộ lọc, đọc thông tin từng nhà, xem thông tin cá nhân của các người dùng có tài khoản đã được kích hoạt, đăng ký

Người dùng đã có tài khoản: Đăng nhập, có chức năng của người dùng chưa có tài khoản, quản lý thông tin cá nhân, đăng tin, nạp tiền vào hệ thống để đẩy tin (nạp thẻ điện thoại), yêu thích tin (bỏ yêu thích), xem lịch sử hoạt động của từng tin, thống kê và quản lý lịch sử nạp tiền, quản lý tin cá nhân (đang chờ duyệt, đã bị hủy duyệt, đang bị khóa)

Admin: Đăng nhập, đăng xuất, quản lý mật khẩu, quản lý thông tin các người dùng, quản lý tin, thực hiện chức năng duyệt tin, ẩn tin, khóa tin, hủy yêu cầu duyệt tin, quản lý tài chính của hệ thống

Công nghệ sử dụng:

Back-end: Postgresql, python 3, django 3
Front-end: Html, css, scss, javascript (es6), Fetch-Api, bootstrap
