from dash import Dash, html, dcc, callback, Input, Output
import dash


app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	

    html.Nav(className= 'topnav', children = 
        [
                    dcc.Link('Match Stats', id = 'link1', href=dash.page_registry['pages.html_prem']['path']),
		            dcc.Link('Player Stats',id = 'link2', href=dash.page_registry['pages.html_players']['path']),
			        dcc.Link('Team Stats',id = 'link3', href=dash.page_registry['pages.html_team']['path'])
                
                
        ]
    ),
    html.Div([
        html.Img(id = 'prem_logo', src='https://seeklogo.com/images/P/premier-league-new-logo-D22A0CE87E-seeklogo.com.png'),
    ], style = {'text-align': 'center'}),

    dash.page_container,
 
	
])


if __name__ == '__main__':
	app.run_server(debug=False)