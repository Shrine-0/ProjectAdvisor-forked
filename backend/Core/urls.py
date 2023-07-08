from django.urls import path

from Core.views import QueryDateRangeView,QueryDayGraph, QueryWeekGraph, QueryMonthGraph,QueryYearGraph, QueryCategoryMonthView, QueryCategoryDayView, QueryCategoryWeekView, QueryCategoryCustomView, QueryCategoryYearView, QueryDayIncomeGraph, QueryWeekIncomeGraph, QueryMonthIncomeGraph, QueryYearIncomeGraph, QueryDayNetView, QueryWeeklyNetView, QueryMonthNetView, QueryYearNetView, QueryIncomeCategoryDayView, QueryIncomeCategoryWeekView, QueryIncomeCategoryMonthView, QueryIncomeCategoryYearView, QueryIncomeCategoryCustomView

app_name = "core"

urlpatterns = [
    
    # Urls fetches all the Expenses based on Expenses_Category
    path("expenses-category-range/",QueryCategoryCustomView.as_view(), name="custom-Category"),
    path("expenses-category-day/",QueryCategoryDayView.as_view(), name="Today-Category"),
    path("expenses-category-week/",QueryCategoryWeekView.as_view(), name="week-Category"),
    path("expenses-category-month/", QueryCategoryMonthView.as_view(), name="Month-query_category"),
    path("expenses-category-year/", QueryCategoryYearView.as_view(), name="Year-query_category"),
    
    
    # Urls fetches all the Income based on Income_Category
    path("income-category-range/",QueryIncomeCategoryCustomView.as_view(), name="custom-Category"),
    path("income-category-day/",QueryIncomeCategoryDayView.as_view(), name="Today-Income_Category"),
    path("income-category-week/",QueryIncomeCategoryWeekView.as_view(), name="Week-Income_Category"),
    path("income-category-month/", QueryIncomeCategoryMonthView.as_view(), name="Month-Income_Category"),
    path("income-category-year/", QueryIncomeCategoryYearView.as_view(), name="Year-Income_Category"),
    
    
    
    # These URLS fetches all the Expenses or Income details    
    path("query-date-range/", QueryDateRangeView.as_view(), name="query_date_range"),
    
    
    # These URLS fetches all the Expenses details
    path("expenses-day-graph/", QueryDayGraph.as_view(), name="Per Day detials"),
    path("expenses-week-graph/", QueryWeekGraph.as_view(), name="Last 7 Day"),
    path("expenses-month-graph/", QueryMonthGraph.as_view(), name="Current Month Graph"),
    path("expenses-year-graph/", QueryYearGraph.as_view(), name="Yearly Graph"),


    
    # These URLS fetches all the Income details
    path("income-day-graph/", QueryDayIncomeGraph.as_view(), name="per day Income"),
    path("income-week-graph/", QueryWeekIncomeGraph.as_view(), name="Last 7 Day Income"),
    path("income-month-graph/", QueryMonthIncomeGraph.as_view(), name="Current Month Graph"),
    path("income-year-graph/", QueryYearIncomeGraph.as_view(), name="Yearly Graph"),


    # These URLS fetches all the Net values 
    path("query-day-net/", QueryDayNetView.as_view(), name="query_day_net"),
    path("query-week-net/", QueryWeeklyNetView.as_view(), name="query_weekly_net"),
    path("query-month-net/", QueryMonthNetView.as_view(), name="query_month_net"),
    path("query-year-net/", QueryYearNetView.as_view(), name="query_year_net"),
    
]