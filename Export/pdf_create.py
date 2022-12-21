def download_report():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT * FROM employee")
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)

        col_width = page_width / 4
        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['id']), border=1)
            pdf.cell(col_width, th, row['name'], border=1)
            pdf.cell(col_width, th, row['position'], border=1)
            pdf.cell(col_width, th, row['office'], border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10.0)
        pdf.cell(page_width, 0.0, '- end of report -', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
#
