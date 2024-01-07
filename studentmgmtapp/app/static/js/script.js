/*
Author       : Dreamguys
Template Name: Preskool - Bootstrap Admin Template
Version      : 1.0
*/

(function($) {
    "use strict";

	// Variables declarations

	var $wrapper = $('.main-wrapper');
	var $pageWrapper = $('.page-wrapper');
	var $slimScrolls = $('.slimscroll');

	// Sidebar

	var Sidemenu = function() {
		this.$menuItem = $('#sidebar-menu a');
	};

	function init() {
		var $this = Sidemenu;
		$('#sidebar-menu a').on('click', function(e) {
			if($(this).parent().hasClass('submenu')) {
				e.preventDefault();
			}
			if(!$(this).hasClass('subdrop')) {
				$('ul', $(this).parents('ul:first')).slideUp(350);
				$('a', $(this).parents('ul:first')).removeClass('subdrop');
				$(this).next('ul').slideDown(350);
				$(this).addClass('subdrop');
			} else if($(this).hasClass('subdrop')) {
				$(this).removeClass('subdrop');
				$(this).next('ul').slideUp(350);
			}
		});
		$('#sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
	}

	// Sidebar Initiate
	init();

	// Mobile menu sidebar overlay

	$('body').append('<div class="sidebar-overlay"></div>');
	$(document).on('click', '#mobile_btn', function() {
		$wrapper.toggleClass('slide-nav');
		$('.sidebar-overlay').toggleClass('opened');
		$('html').addClass('menu-opened');
		return false;
	});

	// Sidebar overlay

	$(".sidebar-overlay").on("click", function () {
		$wrapper.removeClass('slide-nav');
		$(".sidebar-overlay").removeClass("opened");
		$('html').removeClass('menu-opened');
	});

	// Page Content Height

	if($('.page-wrapper').length > 0 ){
		var height = $(window).height();
		$(".page-wrapper").css("min-height", height);
	}

	// Page Content Height Resize

	$(window).resize(function(){
		if($('.page-wrapper').length > 0 ){
			var height = $(window).height();
			$(".page-wrapper").css("min-height", height);
		}
	});

	// Select 2

    if ($('.select').length > 0) {
        $('.select').select2({
            minimumResultsForSearch: -1,
            width: '100%'
        });
    }

	// Datetimepicker

	if($('.datetimepicker').length > 0 ){
		$('.datetimepicker').datetimepicker({
			format: 'DD-MM-YYYY',
			icons: {
				up: "fas fa-angle-up",
				down: "fas fa-angle-down",
				next: 'fas fa-angle-right',
				previous: 'fas fa-angle-left'
			}
		});
		$('.datetimepicker').on('dp.show',function() {
			$(this).closest('.table-responsive').removeClass('table-responsive').addClass('temp');
		}).on('dp.hide',function() {
			$(this).closest('.temp').addClass('table-responsive').removeClass('temp')
		});
	}

	// Tooltip

	if($('[data-toggle="tooltip"]').length > 0 ){
		$('[data-toggle="tooltip"]').tooltip();
	}

    // Datatable

//    if ($('.datatable').length > 0) {
//        $('.datatable').Datables({
//            "bFilter": false,
//        });
//    }

    $(document).ready(function() {
        $('#dshocsinh').DataTable();
    });

    $(document).ready(function() {
        $('#dslop').DataTable();
    });

    $(document).ready(function() {
        $('#dsmonhoc').DataTable();
    });

	// Summernote

	if($('.summernote').length > 0) {
		$('.summernote').summernote({
			height: 200,                 // set editor height
			minHeight: null,             // set minimum height of editor
			maxHeight: null,             // set maximum height of editor
			focus: false                 // set focus to editable area after initializing summernote
		});
	}


	// Sidebar Slimscroll

	if($slimScrolls.length > 0) {
		$slimScrolls.slimScroll({
			height: 'auto',
			width: '100%',
			position: 'right',
			size: '7px',
			color: '#ccc',
			allowPageScroll: false,
			wheelStep: 10,
			touchScrollStep: 100
		});
		var wHeight = $(window).height() - 60;
		$slimScrolls.height(wHeight);
		$('.sidebar .slimScrollDiv').height(wHeight);
		$(window).resize(function() {
			var rHeight = $(window).height() - 60;
			$slimScrolls.height(rHeight);
			$('.sidebar .slimScrollDiv').height(rHeight);
		});
	}

	// Small Sidebar

	$(document).on('click', '#toggle_btn', function() {
		if($('body').hasClass('mini-sidebar')) {
			$('body').removeClass('mini-sidebar');
			$('.subdrop + ul').slideDown();
		} else {
			$('body').addClass('mini-sidebar');
			$('.subdrop + ul').slideUp();
		}
		setTimeout(function(){
			mA.redraw();
			mL.redraw();
		}, 300);
		return false;
	});
	$(document).on('mouseover', function(e) {
		e.stopPropagation();
		if($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
			var targ = $(e.target).closest('.sidebar').length;
			if(targ) {
				$('body').addClass('expand-menu');
				$('.subdrop + ul').slideDown();
			} else {
				$('body').removeClass('expand-menu');
				$('.subdrop + ul').slideUp();
			}
			return false;
		}
	});

	// Circle Progress Bar
	function animateElements() {
		$('.circle-bar1').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph1').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph1').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#6e6bfa'
					}
				});
			}
		});
		$('.circle-bar2').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph2').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph2').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#6e6bfa'
					}
				});
			}
		});
		$('.circle-bar3').each(function () {
			var elementPos = $(this).offset().top;
			var topOfWindow = $(window).scrollTop();
			var percent = $(this).find('.circle-graph3').attr('data-percent');
			var animate = $(this).data('animate');
			if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
				$(this).data('animate', true);
				$(this).find('.circle-graph3').circleProgress({
					value: percent / 100,
					size : 400,
					thickness: 30,
					fill: {
						color: '#6e6bfa'
					}
				});
			}
		});
	}

	if($('.circle-bar').length > 0) {
		animateElements();
	}
	$(window).scroll(animateElements);

	// Preloader

	$(window).on('load', function () {
		if($('#loader').length > 0) {
			$('#loader').delay(350).fadeOut('slow');
			$('body').delay(350).css({ 'overflow': 'visible' });
		}
	})

})(jQuery);

//Xác nhận tiếp nhận học sinh
$(document).ready(function() {
    $('#tiepnhan').on('click', function() {
        // Hiển thị hộp thoại xác nhận và xử lý kết quả
        var confirmation = confirm('Bạn có chắc chắn muốn tiếp tục?');

        // Kiểm tra kết quả
        if (confirmation) {
            // Nếu người dùng chọn "OK"
           $('#frmtiepnhan').submit();
           alert('Lưu thành công');
        } else {
            // Nếu người dùng chọn "Cancel"
           return false
        }
    });
});
//=================================================================//
//Hiển thị học sinh từng lớp
$(document).ready(function () {
        // Handle select box change event
        $('#classSelector').change(function () {
            // Get the selected class ID
            var selectedClassId = $(this).val();

            // Make an AJAX request to get data for the selected class
            $.ajax({
                url: '/get_data',  // Replace with your Flask route
                type: 'POST',
                data: { 'selected_class_id': selectedClassId },
                success: function (data) {
                    // Update the table with the received data
                    updateTable(data);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });

        // Function to update the table with data
        function updateTable(data) {
            // Clear existing rows
            $('#dataTable tbody').empty();

            // Append new rows
            data.forEach(function (row) {
                var formattedNgaySinh = formatNgaySinh(row.ngaySinh);
                var newRow = '<tr>' +
                    '<td>' + row.id + '</td>' +
                    '<td>' + row.tenHocSinh + '</td>' +
                    '<td>' + row.gioiTinh + '</td>' +
                    '<td>' + formattedNgaySinh  + '</td>' +
                    '<td>' + row.diaChi + '</td>' +
                    '<td><button class="btn-sua-hs btn btn-warning" data-id="' + row.id + '"><i class="fas fa-pen"></i></button></td>' +
                    '</tr>';
                $('#dataTable tbody').append(newRow);
            });
        }
        // Function to format ngaySinh
        function formatNgaySinh(ngaySinh) {
            var date = new Date(ngaySinh);
            var day = date.getDate();
            var month = date.getMonth() + 1;
            var year = date.getFullYear();
            return (day < 10 ? '0' : '') + day + '/' + (month < 10 ? '0' : '') + month + '/' + year;
        }
    });

//================================================================================================//

// Chỉnh sửa lớp
function hienThiDanhSachLopHoc() {
    $.ajax({
        url: '/get_danh_sach_lop',  // Địa chỉ API để lấy danh sách lớp học
        type: 'GET',
        success: function (data) {
            var tableBody = $('#lop-table-body');
            tableBody.empty();
            data.forEach(function (lop) {
                var row = '<tr>' +
                          '<td>' + lop.id + '</td>' +
                          '<td>' + lop.tenLop + '</td>' +
                          '<td>' + lop.siSo + '</td>' +
                          '<td><button class="btn-sua btn btn-warning" data-id="' + lop.id + '">Chỉnh Sửa</button></td>' +
                          '</tr>';
                tableBody.append(row);
            });

            // Bắt sự kiện khi nút "Chỉnh Sửa" được click
            $('.btn-sua').click(function () {
                var lopId = $(this).data('id');
                hienFormChinhSua(lopId);
            });

            // Bắt sự kiện khi nút "Xóa" được click
            $('.btn-xoa').click(function () {
                var lopId = $(this).data('id');
                xoaLopHoc(lopId);
            });
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Function để hiển thị form chỉnh sửa thông tin lớp học
function hienFormChinhSua(lopId) {
    $.ajax({
        url: '/get_lop/' + lopId,  // Địa chỉ API để lấy thông tin lớp học
        type: 'GET',
        success: function (data) {
            // Hiển thị thông tin lớp học trong form
            $('#tenLop').val(data.tenLop);
            $('#siSo').val(data.siSo);

            // Bắt sự kiện khi nút "Lưu" được click
            $('#editForm').submit(function (e) {
                e.preventDefault();
                capNhatThongTinLopHoc(lopId);
                $('#editModal').modal('hide');  // Ẩn modal sau khi cập nhật
            });

            // Hiển thị modal chỉnh sửa
            $('#editModal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Function để cập nhật thông tin lớp học
function capNhatThongTinLopHoc(lopId) {
    var tenLopMoi = $('#tenLop').val();
    var siSoMoi = $('#siSo').val();

    // Kiểm tra sĩ số tối đa được phép (ví dụ: 50)
    if (parseInt(siSoMoi) > 40) {
        alert('Sĩ số vượt quá giới hạn. Vui lòng chọn sĩ số dưới 40.');
        return hienFormChinhSua(lopId);
    }

    $.ajax({
        url: '/sua_lop/' + lopId,  // Địa chỉ API để cập nhật thông tin lớp học
        type: 'POST',
        data: { 'ten_lop': tenLopMoi, 'si_so': siSoMoi },
        success: function (response) {
            alert('Thông tin lớp học đã được cập nhật thành công.');
            // Hiển thị lại danh sách lớp học
            hienThiDanhSachLopHoc();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Thực hiện khi trang web được tải xong
$(document).ready(function () {
    // Hiển thị danh sách lớp học khi trang web được tải
    hienThiDanhSachLopHoc();
});

 function xoaLopHoc(lopId) {
        // Hiển thị alert xác nhận trước khi xóa
        var xacNhanXoa = confirm('Bạn có chắc chắn muốn xóa lớp học này?');

        if (xacNhanXoa) {
            // Nếu người dùng chọn "OK", thực hiện xóa
            $.ajax({
                url: '/xoa_lop/' + lopId,  // Địa chỉ API để xóa lớp học
                type: 'DELETE',
                success: function (response) {
                    alert('Lớp học đã được xóa thành công.');
                    // Hiển thị lại danh sách lớp học
                    hienThiDanhSachLopHoc();
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
    }

//=======================================================================================================//