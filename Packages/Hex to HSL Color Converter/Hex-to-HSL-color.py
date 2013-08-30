import sublime, sublime_plugin, re, string

class hex_to_hslCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		self.edit = edit

		for region in self.view.sel():
			self.region = region
			self.word_reg = self.view.word(region)
			if not self.word_reg.empty(): self.convert_to_hsl()


	def rgb_to_hsl(self,r,g,b):
		# From http://sebsauvage.net/python/snyppets/#hsl

		if not (0 <= r <=255): raise ValueError("r (red) parameter must be between 0 and 255.")
		if not (0 <= g <=255): raise ValueError("g (green) parameter must be between 0 and 255.")
		if not (0 <= b <=255): raise ValueError("b (blue) parameter must be between 0 and 255.")

		var_R = r/255.0
		var_G = g/255.0
		var_B = b/255.0

		var_Min = min( var_R, var_G, var_B )    # Min. value of RGB
		var_Max = max( var_R, var_G, var_B )    # Max. value of RGB
		del_Max = var_Max - var_Min             # Delta RGB value

		l = ( var_Max + var_Min ) / 2.0
		h = 0.0
		s = 0.0
		if del_Max!=0.0:
			if l<0.5: s = del_Max / ( var_Max + var_Min )
			else:     s = del_Max / ( 2.0 - var_Max - var_Min )
			del_R = ( ( ( var_Max - var_R ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
			del_G = ( ( ( var_Max - var_G ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
			del_B = ( ( ( var_Max - var_B ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
			if    var_R == var_Max : h = del_B - del_G
			elif  var_G == var_Max : h = ( 1.0 / 3.0 ) + del_R - del_B
			elif  var_B == var_Max : h = ( 2.0 / 3.0 ) + del_G - del_R
			while h < 0.0: h += 1.0
			while h > 1.0: h -= 1.0

		return (h,s,l)


	def per_str(self, val):
		if val > 1:
			tmp_val = val
		else:
			tmp_val = round(val * 100)

		return str(int(tmp_val)) + "%"


	def css_hsl(self,h,s,l):
		return "hsl(" + str(int(round(h * 360))) + ", " + self.per_str(s) + ", " + self.per_str(l) + ")"


	def convert_to_hsl(self):

		word = self.view.substr(self.word_reg)

		re_hex_color = re.compile('([0-9a-fA-F]{3}([0-9a-fA-F]{3})?){1}$')
		match = re_hex_color.match(word)

		if match and self.view.substr(self.word_reg.begin() - 1) == "#":

			word_len = len(word)

			if word_len == 6:
				r,g,b = tuple(int(word[i:i+2], 16) for i in range(0, 6, 2))
			else:
				r,g,b = tuple(int(word[i:i+1], 16)*17 for i in range(0, 3))

			h,s,l = self.rgb_to_hsl(r,g,b)
			tmp_css_hsl = self.css_hsl(h,s,l)

			tmp_reg = sublime.Region(self.word_reg.begin() - 1, self.word_reg.end())

			self.view.replace(self.edit, tmp_reg, tmp_css_hsl)

			return True


