from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8
from bokeh.embed import components
import pandas
from tracker.models import Country
from django.core.management.base import BaseCommand


df_ = pandas.DataFrame(list(Country.objects.all().values()))


class Command(BaseCommand):
	help = "graph"
	def handle(self, *args, **options):

		df = df_
		cas = df['cases'].values
		l=[]
		for i in cas:
			q=i.replace(",","")
			q=int(q)
			l.append(q)
		df['cases'] = l
		source = ColumnDataSource(df)

		output_file('templates/graph_temp.html')

		country_list = source.data['name'].tolist()

		p = figure(
    		y_range=country_list,
    		plot_width=2000,
    		plot_height=3200,
    		title='Coronavirus Cases',
    		x_axis_label='Cases',
    		tools="pan,box_select,zoom_in,zoom_out,save,reset"
		)

		p.hbar(
    		y='name',
    		right='cases',
    		left=0,
    		height=0.7,
    		fill_color=factor_cmap(
      		'name',
      		palette=Blues8,
      		factors=country_list
    		),
    		fill_alpha=0.9,
    		source=source,
		)

		hover = HoverTool()
		hover.tooltips = """
  		<div>
    		<h3>@name</h3>
    		<div><strong>Cases: </strong>@cases</div>
    		<div><strong>Deaths: </strong>@deaths</div>
    		<div><strong>Recovered: </strong>@recovered</div>
    		<div><strong>Tests: </strong>@tests</div>
  		</div>
		"""
		p.add_tools(hover)

		script, div = components(p)

		save(p)


















