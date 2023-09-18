from django.db import models
import pandas as pd
import pickle
import numpy as np
import os,sys

class Client(models.Model):

	status_options = {
		'1': "Шоты жоқ",
		'2': "... < 0₸",
		'3': "0₸ <= ... < 100 000₸",
		'4': "... >= 100 000₸ және расталған жалақысы бар"
	}

	credit_history_options = {
		'0': "Басқа банктерде несиелері бар",
		'1': "Бұрында несиені уақытылы төлемеген",
		'2': "Қазіргі несиелерді тиісті түрде төлеуде",
		'3': "Осы банктегі барлық несиелері тиісті түрде қайтарылды",
		'4': "Несие алмаған/ барлық несиелер тиісті түрде қайтарылған"
	}

	purpose_options = {
		'0': "БАСҚА",
		'1': "КӨЛІК (ЖАҢА)",
		'2': "КӨЛІК (ПАЙДАЛАНҒАН)",
		'3': "ЖИБАЗ/ЖАБДЫҚ",
		'4': "ТҰРМЫСТЫҚ ТЕХНИКА",
		'5': "ТҰРМЫСТЫҚ ҚҰРАЛДАР",
		'6': "ЖӨНДЕУ",
		'7': "ОҚУ",
		'8': "ДЕМАЛЫС",
		'9': "КВАЛИФИКАЦИЯ КӨТЕРУ",
		'10': "БИЗНЕС"
	}

	savings_options = {
		'1': "БЕЛГІСІЗ/ЖИНАҚ ШОТЫ ЖОҚ",
		'2': "... < 50 000₸",
		'3': "50 000₸<= ... < 300 000₸",
		'4': "300 000₸ <= ... < 600 000₸",
		'5': "... >= 600 000₸"
	}

	employment_options = {
		'1': "Жұмыссыз",
		'2': "... < 1 жыл",
		'3': "1 жыл<= ... < 4 жыл",
		'4': "4 жыл<= ... < 7 жыл",
		'5': ".. >= 7 жыл"
	}

	installment_options = {
		'1': ">= 35%",
		'2': "25% <= ...",
		'3': "20% <= ... ",
		'4': "< 20%"
	}

	property_options = {
		'1': "БЕЛГІСІЗ / МҮЛІК ЖОҚ",
		'2': "КӨЛІК НЕМЕСЕ БАСҚА",
		'3': "МҮЛІГІ БАР, ӨМІР САҚТАНДЫРУ",
		'4': "ЖЫЛЖЫМАЙТЫН МҮЛІК"
	}

	credits_options = {
		'1': "1",
		'2': "2-3",
		'3': "4-5",
		'4': ">=6"
	}

	job_options = {
		'1': "жұмыссыз/ білікті емес - резидент емес",
		'2': "білікті емес – резидент",
		'3': "білікті қызметкер/шенеунік",
		'4': "басшы/ өзін-өзі жұмыспен қамтыған/жоғары білікті қызметкер/ офицер"
	}

	telephone_options = {
		'1': "Жоқ",
		'2': "Иә, тұтынушының атына тіркелген"
	}

	personal_status_sex_options = {
		'1': "Еркек: ажырасқан",
		'2': "Әйел: ажырасқан",
		'3': "Еркек: бойдақ",
		'4': "Ер адам/Әйел: үйленген",
		'5': "Әйел: жалғызбасты"
	}

	RES_CHOICES = (
		('БЕЛГІСІЗ', 'Белгісіз'),
		('ЖОҚ', 'Жоқ'),
		('ИӘ', 'Иә'),
	)

	iin = models.CharField("ЖСН", max_length=100, default ='0')
	name = models.CharField("Аты-жөні",max_length=100, default ='Unknown')
	status = models.CharField("Шот статусы",max_length=100, choices=status_options.items())
	duration = models.IntegerField("Кредиттеу мерзімі")
	credit_history = models.CharField("Кредит тарихы", max_length=100, choices=credit_history_options.items())
	purpose = models.CharField("Мақсаты", max_length=100, choices=purpose_options.items())
	amount = models.IntegerField("Сомасы",)
	savings = models.CharField("Сақталған қаржысы", max_length=100, choices=savings_options.items())
	employment_duration = models.CharField("Жұмыс істеу мерзімі", max_length=100, choices=employment_options.items())
	installment_rate = models.CharField("Сыйақы мөлшерлемелері", max_length=100, choices=installment_options.items())
	personal_status_sex = models.CharField("Жеке статусы", max_length=100, choices=personal_status_sex_options.items())
	property = models.CharField("Мүлігі", max_length=100, choices=property_options.items())
	age = models.IntegerField("Жасы")
	number_credits = models.CharField("Несиелерінің саны", max_length=100, choices=credits_options.items())
	job = models.CharField("Жұмысы", max_length=100, choices=job_options.items())
	people_liable = models.IntegerField('Жауапты адамдар')
	telephone = models.CharField('Телефон', max_length=100, choices=telephone_options.items(), editable=False)
	credit_risk = models.CharField('Несиелік қабілеті', max_length=100, null=True, blank=True)
	credit_score = models.CharField('Несиелік қабілетінің ұпайы', max_length=100, null=True, blank=True)
	is_creditable = models.CharField('Несие ала алады ма?', max_length=100, choices=RES_CHOICES, default='БЕЛГІСІЗ')

	class Meta:
		verbose_name = "Тұтынушы"
		verbose_name_plural = "Тұтынушылар"

	def __str__(self):
		return f"{self.name} - {self.iin}"

	def save(self, *args, **kwargs):

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

		# Моделде қолданылатын файлдардың сақталған орындары
		file_path = os.path.join(BASE_DIR, 'scoring', 'files', 'transformer.pkl')
		file_path_2 = os.path.join(BASE_DIR, 'scoring', 'files', 'model.pkl')

		with open(file_path, 'rb') as t:
			transformer = pickle.load(t)

		with open(file_path_2, 'rb') as f:
			model = pickle.load(f)

		data = np.array([[int(self.status), self.duration, int(self.credit_history), int(self.purpose), int(self.amount/130),
						  int(self.savings), int(self.employment_duration), int(self.installment_rate),
						  int(self.personal_status_sex), int(self.property), self.age, int(self.number_credits),
						  int(self.job), self.people_liable, 2]])

		datat = pd.DataFrame(data, columns=['status', 'duration', 'credit_history', 'purpose', 'amount', 'savings',
											'employment_duration', 'installment_rate', 'personal_status_sex',
											'property', 'age', 'number_credits', 'job', 'people_liable', 'telephone'])

		weights = np.array([-0.5, 0.2, -0.3, 0.1, -0.4, -0.2, 0.3, -0.1, 0.2, 0.3, -0.2, -0.3, 0.1, -0.2, 0.1])

		intercept = 0.5
		weights = weights.reshape(-1, 1)
		credit_risk_rate = np.dot(weights.T, data.T) + intercept
		self.credit_score = str(credit_risk_rate[0, 0]*-1)

		transformed = transformer.transform(datat)
		result = model.predict(np.array(transformed))
		if result == 0:
			self.credit_risk = "Төмен"
			self.is_creditable = "ЖОҚ"
		else:
			self.credit_risk = "Жақсы"
			self.is_creditable = "ИӘ"

		super().save(*args, **kwargs)

	def update(self, *args, **kwargs):
		print(self.people_liable)
		super().update(*args, **kwargs)



class Report(models.Model):

	client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
	report = models.TextField("Түсініктеме", blank=True, null=True)
	date_created = models.DateTimeField('Күні', auto_now_add=True)

	class Meta:
		verbose_name = "Тұтынушы бойынша есеп"
		verbose_name_plural = "Тұтынушылар бойына есептер"

	def __str__(self):
		return f"{self.client} - {self.date_created}"


class Blacklist(models.Model):
	client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
	report = models.TextField("Түсініктеме", blank=True, null=True)
	date_created = models.DateTimeField('Күні', auto_now_add=True)
	is_black = models.BooleanField('Қара тізімде ме?', default=False)

	class Meta:
		verbose_name = "Қара тізім"
		verbose_name_plural = "Қара тізім"

	def __str__(self):
		return f"{self.client} - {self.date_created}"



