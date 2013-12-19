import Frontend

def OnEnable(**kwargs):
	args = []

	for conf in ['Server', 'Port', 'Name', 'NamePass', 'Chan']:
		item = kwargs["conf"]['IRC.' + conf]

		if item == None:
			Severe('No IRC.' + conf + ' in config')

			raise Exception('No IRC.' + conf + ' in config')

		args.append(item)

	Frontend.Init(*args)

def OnDisable(**kwargs):
	Frontend.Terminate()	

