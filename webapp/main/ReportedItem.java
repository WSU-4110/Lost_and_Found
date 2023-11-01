package webapp.main;

import java.time.LocalDate;

public class ReportedItem {
    private String itemname;
    private String brand;
    private String reportDate;
    private String location;
    private String category;
    private String description;

    public ReportedItem(String itemname, String brand, String reportDate, String location, String category, String description) {
        this.itemname = itemname;
        this.brand = brand;
        this.reportDate = reportDate;
        this.location = location;
        this.category = category;
        this.description = description;
    }

    public void setItemname(String itemname) {
        this.itemname = itemname;
    }
    public String getItemname() {
        return this.itemname;
    }
    public void setBrand(String brand) {
        this.brand = brand;
    }
    public String getBrand() {
        return this.brand;
    }
    public void seReportDate(String reportDate) {
        this.reportDate = reportDate;
    }
    public String getReportDate() {
        return this.reportDate;
    }
    public void setLocation(String location) {
        this.location = location;
    }
    public String getLocation() {
        return this.location;
    }
    public void setCategory(String category) {
        this.category = category;
    }
    public String getCategory() {
        return this.category;
    }
    public void setDescription(String description) {
        this.description = description;
    }
    public String getDescription() {
        return this.description;
    }
    

}

interface Field_Validation {
    boolean checktextfield(String item);
    boolean checkdescriptionfield(String description);
    boolean checkdate(String date);
}


class formAuth implements Field_Validation {

    @Override
    public boolean checktextfield(String textField) {
        int length = textField.length();
        if (length <= 50){
            return true;
        }
        else 
        {
            return false;
        }
    }

    @Override
    public boolean checkdescriptionfield(String description) {
        int length = description.length();
        if (length <= 500){
            return true;
        }
        else 
        {
            return false;
        }
    }

    @Override
    public boolean checkdate(String dateinput) {

      LocalDate today = LocalDate.now();
      LocalDate pastDate = LocalDate.parse(dateinput);
      boolean isAfter = today.isAfter(pastDate);	
      return !isAfter;	

    }
}