from sqlalchemy import create_engine, text
from .llm_process import date_format_processor, date_format_convertor, currency_format_check, currency_get_format, currency_convertor, currency_exchange
import oracledb


class formatter:
    def __init__(self):
        self.thin_connection = self.db_thin_connection(
            user="TEST_SCHEMA",
            password="Conneq_schema1",
            dsn="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.ap-mumbai-1.oraclecloud.com))(connect_data=(service_name=ge39e7b01ee1b6f_connetqdevdb_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))",
            min=1,
            max=5,
            increment=1,
        )

    def db_thin_connection(self, user, password, dsn, min=1, max=5, increment=1):
        print("connecting")
        try:
            ConnectionPool = oracledb.create_pool(
                user=user,
                password=password,
                dsn=dsn,
                min=min,
                max=max,
                increment=increment,
            )
            engine = create_engine("oracle+oracledb://", creator=ConnectionPool.acquire)
            return engine
        except Exception as e:
            print(f"DB Error:  {e}")
            return None

    def run_query(self):
        print("querying")
        try:
            query = """SELECT requested_delivery_date, need_identification_date, ACTUAL_OR_ESTIMATED
                    FROM dpw_file_extract
                    ORDER BY CAST(CREATION_DATE AS DATE) DESC FETCH FIRST 2 ROWS ONLY"""
            with self.thin_connection.connect() as conn:
                result = conn.execute(text(query))
                data = result.fetchall()
                return data
        except Exception as e:
            print(f"Error: {e}")
            return ""


def format_changer(
    requested_delivery_date, need_identification_date, actual_or_estimated
):
    formatter = formatter().run_query()
    # formatter = [('Jan 05 2023', 'December 2022', 'USD 950,000'), ('02/01/23', 'January 2024', 'USD 38,250')]
    actual_or_estimated_num_list = actual_or_estimated.split()
    actual_or_estimated_num_value = float([num for num in actual_or_estimated_num_list if num.isdigit()][0])
    data_dict = {
        "requested_delivery_date": [],
        "need_identification_date": [],
        "actual_or_estimated": [],
    }

    for i in formatter:
        data_dict["requested_delivery_date"].append(i[0])
        data_dict["need_identification_date"].append(i[1])
        data_dict["actual_or_estimated"].append(i[2])

    old_dates_similarity_requested_delivery_dates = date_format_processor(
        data_dict["requested_delivery_date"][0], data_dict["requested_delivery_date"][1]
    )
    old_dates_similarity_need_identification_date = date_format_processor(
        data_dict["need_identification_date"][0],
        data_dict["need_identification_date"][1],
    )
    old_currency_similarity = currency_format_check(
        data_dict["actual_or_estimated"][0], data_dict["actual_or_estimated"][1]
    )
    if old_dates_similarity_requested_delivery_dates["format"].upper() == "YES":
        date_similarity_check = date_format_processor(
            data_dict["requested_delivery_date"][0], requested_delivery_date
        )
        if date_similarity_check["format"].upper() == "NO":
            requested_delivery_date = date_format_convertor(
                requested_delivery_date, data_dict["requested_delivery_date"][0]
            )["format"]
    if old_dates_similarity_need_identification_date["format"].upper() == "YES":
        date_similarity_check = date_format_processor(
            data_dict["need_identification_date"][0], need_identification_date
        )
        if date_similarity_check["format"].upper() == "NO":
            need_identification_date = date_format_convertor(
                need_identification_date, data_dict["need_identification_date"][0]
            )["format"]
    if old_currency_similarity["same"].upper() == "YES":
        currency_similarity = currency_format_check(
            actual_or_estimated, data_dict["actual_or_estimated"][0]
        )
        if currency_similarity["same"].upper() == "NO":
            actual_or_estimated_dict = currency_get_format(
                actual_or_estimated, data_dict["actual_or_estimated"][0]
            )
            actual_or_estimated = y = "{:.2f}".format(currency_exchange(
                actual_or_estimated_dict["currency1"],
                actual_or_estimated_dict["currency2"],
                actual_or_estimated_num_value,
            ))
            final_value = ""
            format_list = data_dict["actual_or_estimated"][0].split()
            for i in format_list:
                if any(char.isdigit() for char in i):
                    final_value += str(actual_or_estimated) + " "
                    continue
                final_value += i + " "

            actual_or_estimated = final_value
            
    return requested_delivery_date, need_identification_date, actual_or_estimated


# if __name__ == "__main__":
#     formatter = formatter()
#     sql_data = formatter.run_query()
#     print(sql_data)
#     data_dict = {
#         "requested_delivery_date": [],
#         "need_identification_date": [],
#         "actual_or_estimated": [],
#     }
