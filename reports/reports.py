from .csv import ModelCSVResponse, NewVersionSingleRelationalModelCSVResponse


class OverallResidenceReport(ModelCSVResponse):
    csv_columns = ['الراتب الاساسي', 'بدل غذاء', 'بدل سكن', 'بدل انتقال', 'محموع السلفة',
                   'مجموع عدد ساعات العمل', 'مجموع الخصم', 'محموع المكافئات', 'تكلفة مجموع عدد ساعات العمل',
                   'مجموع البدالات', 'عدد ساعات الغياب', 'مجموع خصم الغياب', 'محموع المترب',
                   'محموع الخصم', 'صافي المرتب']
    csv_fields = ['basic_salary', 'feeding_allowance', 'housing_allowance', 'transporting_allowance', 'total_loans',
                  'total_extra_work_hours', 'total_deduction', 'total_rewards', 'total_extra_work_hours_money',
                  'get_total_allowance', 'total_absence_hours', 'total_absence_deduction', 'total_salary',
                  'total_salary_deduction', 'net_salary']


class SingleMonthReport(NewVersionSingleRelationalModelCSVResponse):
    csv_fields = ['username', ]
    after_csv_fields = ['basic_salary', 'feeding_allowance', 'housing_allowance', 'transporting_allowance',
                        'total_loans', 'total_extra_work_hours', 'total_deduction', 'total_rewards',
                        'total_extra_work_hours_money', 'get_total_allowance', 'total_absence_hours',
                        'total_absence_deduction', 'total_salary', 'total_salary_deduction', 'net_salary']
    csv_model_related_field_name = 'months'
    csv_model_related_fields = ['day_number', 'location',  'attendance', 'extra_work_hours', 'deduction', 'rewards', 'loans', ]


class OneSingleMonthAttendanceReport(ModelCSVResponse):
    csv_columns = ['رقم اليوم',  'الحضور', 'عدد سعات العمل الاضافية', 'الخصم', 'المكافئات', 'السلف']
    csv_fields = ['day_number', 'location',  'attendance', 'extra_work_hours', 'deduction', 'rewards', 'loans']


class OverallVacationReport(ModelCSVResponse):
    csv_columns = ['الاسم', 'بداية من', 'نهاية الي', 'عدد الايام', 'سبب الغياب']
    csv_fields = ['username',  'start_date', 'end_date', 'duration_in_days', 'reason']
