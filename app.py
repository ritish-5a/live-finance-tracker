# --- AI PREDICTION SECTION ---
st.divider()
st.subheader("🤖 AI Expense Forecasting")

if st.button("Predict Next Month's Expenses"):
    if len(df) < 2:
        st.error("Not enough data! Please add expenses from at least 2 different months to see a trend.")
    else:
        try:
            # 1. Data Processing
            df['Date'] = pd.to_datetime(df['Date'])
            monthly_df = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum().reset_index()
            monthly_df['Month_Number'] = np.arange(len(monthly_df)) + 1

            # 2. ML Training
            X = monthly_df[['Month_Number']]
            y = monthly_df['Amount']
            model = LinearRegression()
            model.fit(X, y)

            # 3. Prediction
            next_month_num = monthly_df['Month_Number'].max() + 1
            prediction = model.predict([[next_month_num]])

            # 4. Show Result
            st.success(f"### Predicted spending for next month: **${prediction[0]:,.2f}**")
            st.write("How this works: The AI uses **Linear Regression** to analyze your monthly spending growth/decline and projects that trend into the next month.")
            
        except Exception as e:
            st.error(f"Error calculating prediction: {e}")
