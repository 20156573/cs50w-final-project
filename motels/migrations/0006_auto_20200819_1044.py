# Generated by Django 3.0.7 on 2020-08-19 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0005_auto_20200814_2357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'Loại tin: cho căn chung cư', 'verbose_name_plural': 'Loại tin: cho thuê căn chung cư'},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'Quận', 'verbose_name_plural': 'Quận'},
        ),
        migrations.AlterModelOptions(
            name='house',
            options={'verbose_name': 'Loại tin: cho thuê nhà nguyên căn', 'verbose_name_plural': 'Loại tin: cho thuê nhà nguyên căn'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Tin đăng', 'verbose_name_plural': 'Tin đăng'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Loại tin: cho thuê pòng trọ', 'verbose_name_plural': 'Loại tin: cho thuê phòng trọ'},
        ),
        migrations.AlterModelOptions(
            name='roommate',
            options={'verbose_name': 'Loại tin: tìm bạn ở ghép', 'verbose_name_plural': 'Loại tin: tìm bạn ở ghép'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Người dùng', 'verbose_name_plural': 'Người dùng'},
        ),
        migrations.AlterField(
            model_name='apartment',
            name='number_of_bedrooms',
            field=models.IntegerField(verbose_name='Số phòng ngủ'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='number_of_toilets',
            field=models.IntegerField(verbose_name='Số phòng vệ sinh'),
        ),
        migrations.AlterField(
            model_name='house',
            name='number_of_bedrooms',
            field=models.IntegerField(verbose_name='Số phòng ngủ'),
        ),
        migrations.AlterField(
            model_name='house',
            name='number_of_toilets',
            field=models.IntegerField(verbose_name='Số phòng vệ sinh'),
        ),
        migrations.AlterField(
            model_name='house',
            name='total_floor',
            field=models.IntegerField(verbose_name='Tổng số tầng'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='photo_post/', verbose_name='Thêm ảnh'),
        ),
        migrations.AlterField(
            model_name='post',
            name='area',
            field=models.FloatField(help_text='<span style="position:absolute;left:205px; top:17px ">m2</span>', verbose_name='Diện tích'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(0, 'Tìm bạn ở ghép'), (1, 'Cho thuê phòng trọ'), (2, 'Cho thuê nhà nguyên căn'), (3, 'Cho thuê nguyên căn chung cư')], verbose_name='Loại bài đăng'),
        ),
        migrations.AlterField(
            model_name='post',
            name='deposit',
            field=models.IntegerField(blank=True, help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>', null=True, verbose_name='Đặt cọc'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Mô tả'),
        ),
        migrations.AlterField(
            model_name='post',
            name='furniture',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Nội thất'),
        ),
        migrations.AlterField(
            model_name='post',
            name='other_contact_info',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Thông tin liên hệ khác'),
        ),
        migrations.AlterField(
            model_name='post',
            name='rent',
            field=models.IntegerField(help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>', verbose_name='Giá thuê nhà/tháng'),
        ),
        migrations.AlterField(
            model_name='post',
            name='renters_gender',
            field=models.IntegerField(choices=[(0, 'Chỉ nữ'), (1, 'Chỉ nam'), (2, 'Tất cả')], help_text='<span style="position:absolute;left:112px; top:17px ">thuê</span>', verbose_name='Ưu tiên'),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(default=1, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=110, verbose_name='Tiêu đề'),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian cập nhật'),
        ),
        migrations.AlterField(
            model_name='room',
            name='max_rent',
            field=models.IntegerField(blank=True, help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>', null=True, verbose_name='Giá thuê dao động tới'),
        ),
        migrations.AlterField(
            model_name='room',
            name='number_of_rooms',
            field=models.IntegerField(blank=True, help_text='<span style="position:absolute;left:205px; top:17px ">phòng</span>', null=True, verbose_name='Bạn còn'),
        ),
        migrations.AlterField(
            model_name='roommate',
            name='number_of_roommate',
            field=models.IntegerField(help_text='<span style="position:absolute;left:205px; top:17px ">người</span>', verbose_name='Bạn tìm'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_address', to='motels.Province', verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.png', null=True, upload_to='avatars/', verbose_name='Ảnh đại diện'),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(auto_now_add=True, verbose_name='Ngày tham gia'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, null=True, verbose_name='Họ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, null=True, verbose_name='Tên'),
        ),
    ]
