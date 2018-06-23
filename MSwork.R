### Getting the data

install.packages("tidyr")
library(tidyr)

GPGdata <- read.csv(file = "companies-house-api/UK_Gender_Pay_Gap_Data_2017_to_2018.csv")

head(GPGdata)

summary(GPGdata)

GPGdata <- GPGdata[!(is.na(GPGdata$CompanyNumber) | GPGdata$CompanyNumber==""), ]


####Matching to constituencies

PCdata <- read.csv(file = "C:/Users/Asus/Dropbox/Megan/Coding/Pay Gap/National_Statistics_Postcode_Lookup_UK.csv")

summary(PCdata)

head(GPGdata$Address)

GPGdata$PC <- gsub("(.*)\n(\\w+\\s+\\w+)$","\\2", GPGdata$Address)

head(GPGdata$PC)

PCdata$PC <- PCdata$Postcode.3

GPG_PCdata <- merge(GPGdata, PCdata, by="PC")


###Constituency pay gaps

library(dplyr)

ConstGaps <- GPG_PCdata %>% 
  group_by(Parliamentary.Constituency.Name) %>%
  mutate(mean(DiffMedianHourlyPercent))

ConstGaps$Constituency.Gap <- ConstGaps$`mean(DiffMedianHourlyPercent)`

LeanValues <- c("Parliamentary.Constituency.Name", "Constituency.Gap")

MapGapData <- ConstGaps[LeanValues]

MapGapDataReduced <- unique(MapGapData)

min(MapGapDataReduced$Constituency.Gap)
max(MapGapDataReduced$Constituency.Gap)
boxplot(MapGapDataReduced$Constituency.Gap)

setdiff(ConstSF$id, MapGapDataReduced$Parliamentary.Constituency.Name)



###Mapping


install.packages(c("rio", "rgeos", "maptools", "mapproj", "rgdal", "ggplot2"))
library(rio)
library(rgeos)
library(maptools)
library(mapproj)
library(rgdal)
library(ggplot2)


ConstSF <- readOGR(dsn = "C:/Users/Asus/Dropbox/Megan/Coding/Pay Gap/ConstituenciesDec17", layer = "Westminster_Parliamentary_Constituencies_December_2017_Full_Clipped_Boundaries_in_the_UK")

ConstSF <- fortify(ConstSF, region = "pcon17nm")

setdiff(ConstSF$id, MapGapDataReduced$Parliamentary.Constituency.Name)


MapofGap <- ggplot()  +
  geom_map(data = MapGapDataReduced , aes(map_id = MapGapDataReduced$Parliamentary.Constituency.Name, fill = MapGapDataReduced$Constituency.Gap),  map = ConstSF) +
  geom_polygon (data = ConstSF, aes(x = long, y = lat, group = group), colour = NA, fill = NA) +
  expand_limits(x = ConstSF$long, y = ConstSF$lat) +
  scale_fill_gradient2 (guide = "colourbar", low = ("green4"), mid = ("white"), high = ("red"), midpoint = 0, na.value = ("gray"))  +
  ggtitle("The Gender Pay Gap across the UK \nby parliamentary constituency")  +
  labs(fill = "The % difference in pay \nbetween women and men", 
       caption = "Constituencies with no companies reporting pay gap data are shown in grey") +
  coord_equal () +
  theme(
    axis.text.x = element_blank(), axis.text.y = element_blank(), 
    axis.ticks = element_blank(), axis.title.x = element_blank(), 
    axis.title.y = element_blank(), 
    panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
    panel.border = element_blank(), panel.background = element_blank(), 
    legend.title = element_text(face = "bold"),
    plot.title = element_text(face = "bold", hjust = 0.5)) 

MapofGap


# The following adds the constituencies that are missing from the pay gap dataframe with NA values, 
# but using these with the map leads to an error


MapGapDataReduced[635,] = c("Belfast East", NA)
MapGapDataReduced[636,] = c("Berwick-upon-Tweed", NA)
MapGapDataReduced[637,] = c("Ceredigion", NA)
MapGapDataReduced[638,] = c("East Antrim", NA)
MapGapDataReduced[639,] = c("East Londonderry", NA)
MapGapDataReduced[640,] = c("Foyle", NA)
MapGapDataReduced[641,] = c("Hackney North and Stoke Newington", NA)
MapGapDataReduced[642,] = c("Liverpool, West Derby", NA)
MapGapDataReduced[643,] = c("North Down", NA)
MapGapDataReduced[644,] = c("Orkney and Shetland", NA)
MapGapDataReduced[645,] = c("Rhondda", NA)
MapGapDataReduced[646,] = c("South Antrim", NA)
MapGapDataReduced[647,] = c("South Down", NA)
MapGapDataReduced[648,] = c("Strangford", NA)
MapGapDataReduced[649,] = c("Torridge and West Devon", NA)
MapGapDataReduced[650,] = c("Ynys Mon", NA)

